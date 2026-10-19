// lf_control.h - de regelaar: lijnpositie -> wielsnelheden -> duty voor de motoren.
//
//   positie (mm) --PID--> snelheidsverschil dv (m/s)
//   snelheidsprofiel (boost/rem) --> basissnelheid v (m/s)
//   v_links = v - dv, v_rechts = v + dv
//   per wiel: duty = voorwaarts (v / (v_per_volt * Vbat)) + PI op de encodersnelheid
//
// Portable C++: wordt 1-op-1 gebruikt door de firmware en door de simulatie.
#pragma once
#include <math.h>
#include "lf_params.h"
#include "lf_sensor.h"

namespace lf {

inline float begrens(float x, float lo, float hi) { return x < lo ? lo : (x > hi ? hi : x); }

struct Ingang {
  float refl[N_SENSOR];   // reflectie per sensor (Sensor::reflectie)
  float dt;               // tijd sinds vorige stap (s)
  float vbat;             // batterijspanning (V)
  float v_links, v_rechts;// gemeten wielsnelheid (m/s), 0 als er geen encoders zijn
};

struct Uitgang {
  float duty_links, duty_rechts;  // -1 .. 1
  float positie_mm, v_doel, dv;
  bool lijn;
};

class Regelaar {
 public:
  Params p;
  Sensor sensor;
  bool rijden = false;

  void reset() {
    integ = 0; vorige_fout = 0; d_gefilterd = 0; v_cmd = 0; t_recht = 0;
    i_links = i_rechts = 0; eerste = true;
  }

  Uitgang stap(const Ingang &in) {
    Uitgang u{};
    SensorUit s = sensor.verwerk(in.refl, p);
    u.positie_mm = s.positie_mm;
    u.lijn = s.lijn;
    if (!rijden || in.dt <= 0) { reset(); return u; }

    // --- PID op de lijnpositie
    float fout = s.positie_mm;
    if (eerste) { vorige_fout = fout; eerste = false; }
    float d = (fout - vorige_fout) / in.dt;
    d_gefilterd += p.d_filter * (d - d_gefilterd);
    vorige_fout = fout;
    integ = begrens(integ + fout * in.dt, -50, 50);
    float dv = p.kp * fout + p.ki * integ + p.kd * d_gefilterd;

    // --- snelheidsprofiel: boost op rechte stukken, meteen remmen bij een bocht
    float af = fabsf(fout);
    if (af < p.e_recht) t_recht += in.dt; else t_recht = 0;
    float v_doel = p.v_bocht;
    if (t_recht > p.t_boost) v_doel = p.v_recht;
    if (af > p.e_bocht || fabsf(d_gefilterd) > p.d_rem || !s.lijn) { v_doel = p.v_bocht; t_recht = 0; }
    if (!s.lijn) v_doel *= 0.6f;
    if (v_doel > v_cmd) v_cmd = fminf(v_doel, v_cmd + p.a_boost * in.dt);   // geleidelijk versnellen
    else v_cmd = v_doel;                                                    // remmen = meteen

    dv = begrens(dv, -2 * v_cmd - 0.5f, 2 * v_cmd + 0.5f);
    float vl = v_cmd - dv, vr = v_cmd + dv;

    u.duty_links = wiel(vl, in.v_links, in.vbat, in.dt, i_links);
    u.duty_rechts = wiel(vr, in.v_rechts, in.vbat, in.dt, i_rechts);
    u.v_doel = v_cmd;
    u.dv = dv;
    return u;
  }

 private:
  float integ = 0, vorige_fout = 0, d_gefilterd = 0, v_cmd = 0, t_recht = 0;
  float i_links = 0, i_rechts = 0;
  bool eerste = true;

  float wiel(float v_doel, float v_gemeten, float vbat, float dt, float &i_acc) {
    float vmax = p.v_per_volt * (vbat > 1 ? vbat : 7.4f);   // batterijcompensatie
    float duty = v_doel / vmax;                              // voorwaartse sturing
    if (p.encoders > 0.5f) {
      float fout = v_doel - v_gemeten;
      i_acc = begrens(i_acc + p.ki_v * fout * dt, -0.5f, 0.5f);
      duty += p.kp_v * fout + i_acc;
    }
    return begrens(duty, -1, 1);
  }
};

}  // namespace lf
