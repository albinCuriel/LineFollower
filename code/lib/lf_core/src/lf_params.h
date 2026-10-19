// lf_params.h - alle instelbare parameters van de linefollower.
// Portable C++ (geen Arduino): dezelfde code draait op de ESP32 en in de simulatie (simulatie/).
// Elke parameter is via een commando te lezen/zetten ("set kp 0.05") en wordt bewaard in het flashgeheugen.
#pragma once
#include <stdint.h>
#include <string.h>

namespace lf {

static const int N_SENSOR = 8;
static const float SENSOR_PITCH_MM = 9.525f;   // Pololu QTR-8A
static const float WIEL_D_M = 0.032f;          // Pololu wiel 32x7
static const float SPOOR_M = 0.099f;           // afstand tussen de wielmiddens
static const float TELLEN_PER_TOER = 280.0f;   // 7 PPR x 4 (kwadratuur) x 10:1

// Standaardwaarden = resultaat van simulatie/sim.py tune (90 % van de snelheid, 19/10/2026).
struct Params {
  // --- basis (cursus)
  float cyclus_us   = 1000;   // regelcyclus in microseconden
  float debug       = 0;      // 1 = meetwaarden doorsturen
  // --- lijnregeling: fout = lijnpositie in mm (+ = lijn links), uitgang = snelheidsverschil in m/s
  float kp          = 0.0267f;
  float ki          = 0.0214f;
  float kd          = 0.00145f;
  float d_filter    = 0.5f;   // 0..1, laagdoorlaat op de D-term (1 = geen filter)
  // --- snelheidsprofiel (m/s)
  float v_bocht     = 0.74f;   // snelheid in bochten
  float v_recht     = 2.1f;   // snelheid op rechte stukken (boost)
  float e_recht     = 7.7f;   // |fout| kleiner dan dit (mm) = rechtdoor
  float e_bocht     = 23.6f;   // |fout| groter dan dit (mm) = bocht -> meteen remmen naar v_bocht
  float d_rem       = 171;    // |fout| groeit sneller dan dit (mm/s) = bocht komt eraan -> remmen
  float t_boost     = 0.15f;  // tijd (s) rechtdoor voor de boost begint
  float a_boost     = 7.3f;   // versnelling bij boosten (m/s^2)
  // --- wielsnelheidsregeling (encoders)
  float kp_v        = 0.6f;   // duty per m/s fout
  float ki_v        = 8.0f;   // duty per (m/s * s)
  float v_per_volt  = 0.419f; // onbelaste wielsnelheid per volt (1500 rpm @ 6 V, wiel 32 mm)
  float encoders    = 1;      // 0 = geen encoders: enkel voorwaartse sturing
  // --- veiligheid / sensor
  float vbat_min    = 6.6f;   // onder deze spanning stoppen (3,3 V per cel)
  float lijn_drempel= 350;    // genormaliseerde waarde (0..1000) waaronder een sensor "wit" is
  float led_diff    = 1;      // 1 = meten met IR-leds aan en uit (omgevingslicht wegfilteren)
};

struct Kalibratie {
  float wit[N_SENSOR];        // reflectie op wit  (hoog)
  float zwart[N_SENSOR];      // reflectie op zwart (laag)
  void standaard() {
    for (int i = 0; i < N_SENSOR; i++) { wit[i] = 3000; zwart[i] = 300; }
  }
};

struct ParamDef { const char *naam; float Params::*veld; float min, max; const char *uitleg; };

static const ParamDef PARAM_DEFS[] = {
  {"cycle",    &Params::cyclus_us,   200, 20000, "regelcyclus (us)"},
  {"debug",    &Params::debug,       0, 1,       "meetwaarden doorsturen"},
  {"kp",       &Params::kp,          0, 1,       "P (m/s per mm)"},
  {"ki",       &Params::ki,          0, 10,      "I"},
  {"kd",       &Params::kd,          0, 0.1f,    "D (m/s per mm/s)"},
  {"dfilter",  &Params::d_filter,    0.01f, 1,   "laagdoorlaat D"},
  {"vbocht",   &Params::v_bocht,     0, 4,       "snelheid bocht (m/s)"},
  {"vrecht",   &Params::v_recht,     0, 4,       "snelheid rechtdoor (m/s)"},
  {"erecht",   &Params::e_recht,     0, 40,      "rechtdoor als |fout| < (mm)"},
  {"ebocht",   &Params::e_bocht,     0, 40,      "bocht als |fout| > (mm)"},
  {"drem",     &Params::d_rem,       0, 5000,    "remmen als |dfout/dt| > (mm/s)"},
  {"tboost",   &Params::t_boost,     0, 2,       "wachttijd boost (s)"},
  {"aboost",   &Params::a_boost,     0, 50,      "versnelling boost (m/s2)"},
  {"kpv",      &Params::kp_v,        0, 10,      "P wielsnelheid"},
  {"kiv",      &Params::ki_v,        0, 100,     "I wielsnelheid"},
  {"vpervolt", &Params::v_per_volt,  0.05f, 2,   "wielsnelheid per volt"},
  {"enc",      &Params::encoders,    0, 1,       "encoders gebruiken"},
  {"vbatmin",  &Params::vbat_min,    5, 8.4f,    "minimum batterijspanning"},
  {"drempel",  &Params::lijn_drempel,0, 1000,    "drempel lijn gezien"},
  {"leddiff",  &Params::led_diff,    0, 1,       "meten met leds aan/uit"},
};
static const int N_PARAMS = sizeof(PARAM_DEFS) / sizeof(PARAM_DEFS[0]);

inline const ParamDef *zoek_param(const char *naam) {
  for (int i = 0; i < N_PARAMS; i++)
    if (strcmp(PARAM_DEFS[i].naam, naam) == 0) return &PARAM_DEFS[i];
  return nullptr;
}

// Zet een parameter, begrensd tot [min, max]. Geeft false als de naam niet bestaat.
inline bool zet_param(Params &p, const char *naam, float waarde) {
  const ParamDef *d = zoek_param(naam);
  if (!d) return false;
  if (waarde < d->min) waarde = d->min;
  if (waarde > d->max) waarde = d->max;
  p.*(d->veld) = waarde;
  return true;
}

}  // namespace lf
