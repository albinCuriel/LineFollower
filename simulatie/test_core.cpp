// test_core.cpp - unit tests voor code/lib/lf_core (draaien op de pc, zonder robot).
//   python -m ziglang c++ -std=c++17 -O1 -o test_core.exe test_core.cpp -I ../code/lib/lf_core/src && test_core.exe
#include <stdio.h>
#include <math.h>
#include "lf_core.h"

static int fouten = 0, testen = 0;
#define CHECK(cond, ...) do { testen++; if (!(cond)) { fouten++; printf("FOUT  %s:%d  ", __FILE__, __LINE__); printf(__VA_ARGS__); printf("\n"); } } while (0)

// reflectie voor een lijn (15 mm breed) op positie y_lijn (mm, + = links); sensor i op (3.5 - i) * 9.525
static void meet(float y_lijn, float refl[8]) {
  for (int i = 0; i < 8; i++) {
    float ys = (3.5f - i) * lf::SENSOR_PITCH_MM;
    float d = fabsf(ys - y_lijn);
    float dekking = d < 5.5f ? 1 : (d > 9.5f ? 0 : (9.5f - d) / 4);   // meetvlek r = 2 mm
    refl[i] = 3000 - (3000 - 300) * dekking;
  }
}

int main() {
  lf::Params p;
  lf::Sensor s;
  float r[8];

  // 1. positie volgt de lijn over het hele bereik, met minder dan 3 mm fout
  float max_fout = 0;
  for (float y = -30; y <= 30; y += 0.5f) {
    meet(y, r);
    lf::SensorUit u = s.verwerk(r, p);
    CHECK(u.lijn, "lijn niet gezien op %.1f mm", y);
    max_fout = fmaxf(max_fout, fabsf(u.positie_mm - y));
  }
  CHECK(max_fout < 3.0f, "interpolatiefout %.2f mm (max 3)", max_fout);
  printf("interpolatie: max. fout %.2f mm over -30..+30 mm\n", max_fout);

  // 2. teken: lijn links = positief
  meet(20, r); CHECK(s.verwerk(r, p).positie_mm > 15, "lijn links moet + zijn");
  meet(-20, r); CHECK(s.verwerk(r, p).positie_mm < -15, "lijn rechts moet - zijn");

  // 3. lijn kwijt: onthoudt de laatste kant
  meet(25, r); s.verwerk(r, p);
  for (int i = 0; i < 8; i++) r[i] = 3000;
  lf::SensorUit u = s.verwerk(r, p);
  CHECK(!u.lijn && u.positie_mm > 30, "lijn kwijt links: positie %.1f", u.positie_mm);

  // 4. kruispunt: alles zwart -> vorige positie behouden
  meet(2, r); s.verwerk(r, p);
  for (int i = 0; i < 8; i++) r[i] = 300;
  u = s.verwerk(r, p);
  CHECK(u.kruispunt && fabsf(u.positie_mm - 2) < 3, "kruispunt: positie %.1f", u.positie_mm);

  // 5. kalibratie: andere gevoeligheid per sensor geeft dezelfde positie na kalibratie
  lf::Sensor s2;
  float wit[8], zwart[8];
  for (int i = 0; i < 8; i++) { wit[i] = 2000 + 200 * i; zwart[i] = 200 + 30 * i; }
  s2.kal_wit(wit); s2.kal_zwart(zwart);
  meet(7, r);
  for (int i = 0; i < 8; i++) r[i] = zwart[i] + (wit[i] - zwart[i]) * (r[i] - 300) / 2700;
  CHECK(fabsf(s2.verwerk(r, p).positie_mm - 7) < 3, "gekalibreerde positie %.1f", s2.verwerk(r, p).positie_mm);

  // 6. parameters: set/get en begrenzing
  CHECK(lf::zet_param(p, "kp", 0.05f) && fabsf(p.kp - 0.05f) < 1e-6f, "set kp");
  CHECK(lf::zet_param(p, "kp", 99) && p.kp <= 1.0f, "kp moet begrensd zijn");
  CHECK(!lf::zet_param(p, "bestaatniet", 1), "onbekende parameter moet false geven");
  char regel[] = "set vrecht 1.25", uit[200], *w[4];
  int n = lf::splits(regel, w, 4);
  CHECK(lf::param_commando(p, n, w, uit, sizeof(uit)) && fabsf(p.v_recht - 1.25f) < 1e-6f, "commando set vrecht");

  // 7. regelaar: lijn links -> rechterwiel sneller (naar links draaien); stil = duty 0
  lf::Regelaar g;
  meet(10, r);
  lf::Ingang in{}; for (int i = 0; i < 8; i++) in.refl[i] = r[i];
  in.dt = 0.001f; in.vbat = 7.4f;
  lf::Uitgang o = g.stap(in);
  CHECK(o.duty_links == 0 && o.duty_rechts == 0, "niet rijden = motoren 0");
  g.rijden = true;
  for (int k = 0; k < 50; k++) o = g.stap(in);
  CHECK(o.duty_rechts > o.duty_links, "lijn links: rechts %.2f moet > links %.2f", o.duty_rechts, o.duty_links);

  printf("%d/%d testen geslaagd\n", testen - fouten, testen);
  return fouten ? 1 : 0;
}
