// lf_sensor.h - van ruwe ADC-waarden naar lijnpositie (mm).
// Stappen (cursus): kalibratie -> normalisatie -> interpolatie.
//
// QTR-8A analoog: veel reflectie (wit) = LAGE spanning, weinig reflectie (zwart) = HOGE spanning.
// Met de IR-leds UIT ziet de sensor enkel omgevingslicht. Reflectie = ADC(leds uit) - ADC(leds aan):
// groot op wit, klein op zwart, en omgevingslicht valt weg.
#pragma once
#include <math.h>
#include "lf_params.h"

namespace lf {

struct SensorUit {
  float norm[N_SENSOR];   // 0 = wit .. 1000 = zwart
  float positie_mm;       // + = lijn links van het midden, bereik ongeveer +-33 mm
  bool lijn;              // false = lijn kwijt
  bool kruispunt;         // (bijna) alle sensoren zwart
};

class Sensor {
 public:
  Kalibratie kal;
  float laatste_pos = 0;

  Sensor() { kal.standaard(); }

  // Ruwe metingen -> reflectie (hoog = wit)
  static float reflectie(float adc_aan, float adc_uit, bool led_diff) {
    float r = led_diff ? (adc_uit - adc_aan) : (4095.0f - adc_aan);
    return r < 0 ? 0 : r;
  }

  // Kalibratie: hou het maximum (wit) en minimum (zwart) per sensor bij.
  void kal_start() { for (int i = 0; i < N_SENSOR; i++) { kal.wit[i] = 0; kal.zwart[i] = 1e9f; } }
  void kal_stap(const float refl[N_SENSOR]) {
    for (int i = 0; i < N_SENSOR; i++) {
      if (refl[i] > kal.wit[i]) kal.wit[i] = refl[i];
      if (refl[i] < kal.zwart[i]) kal.zwart[i] = refl[i];
    }
  }
  void kal_wit(const float refl[N_SENSOR])   { for (int i = 0; i < N_SENSOR; i++) kal.wit[i] = refl[i]; }
  void kal_zwart(const float refl[N_SENSOR]) { for (int i = 0; i < N_SENSOR; i++) kal.zwart[i] = refl[i]; }

  SensorUit verwerk(const float refl[N_SENSOR], const Params &p) {
    SensorUit u;
    int imax = 0, n_zwart = 0;
    for (int i = 0; i < N_SENSOR; i++) {
      float bereik = kal.wit[i] - kal.zwart[i];
      if (bereik < 1) bereik = 1;
      float n = 1000.0f * (kal.wit[i] - refl[i]) / bereik;      // normalisatie: zwart = 1000
      u.norm[i] = n < 0 ? 0 : (n > 1000 ? 1000 : n);
      if (u.norm[i] > u.norm[imax]) imax = i;
      if (u.norm[i] > p.lijn_drempel) n_zwart++;
    }
    u.kruispunt = n_zwart >= N_SENSOR - 1;
    u.lijn = u.norm[imax] > p.lijn_drempel;
    if (!u.lijn) {                       // lijn kwijt: onthoud aan welke kant hij verdween
      u.positie_mm = laatste_pos > 0 ? 40.0f : -40.0f;
      return u;
    }
    if (u.kruispunt) {                   // kruispunt: rechtdoor (vorige positie houden)
      u.positie_mm = laatste_pos;
      return u;
    }
    // Interpolatie: zwaartepunt van de zwartwaarden rond de hoogste sensor (+-2 sensoren).
    // De lijn (15 mm) is breder dan de sensorafstand (9,5 mm): vaak zijn 2 sensoren volledig zwart.
    // Een parabool past daar slecht op (tot 5 mm fout); een zwaartepunt niet. Het venster negeert
    // een tweede lijn verderop (kruispunt, ander stuk baan).
    float som = 0, gewogen = 0;
    for (int i = imax - 2; i <= imax + 2; i++) {
      if (i < 0 || i >= N_SENSOR) continue;
      float n = u.norm[i] - 50;                 // ruisvloer
      if (n <= 0) continue;
      som += n; gewogen += n * i;
    }
    float idx = som > 0 ? gewogen / som : (float)imax;
    // sensor 1 (index 0) = uiterst links = +33,3 mm
    u.positie_mm = (3.5f - idx) * SENSOR_PITCH_MM;
    laatste_pos = u.positie_mm;
    return u;
  }
};

}  // namespace lf
