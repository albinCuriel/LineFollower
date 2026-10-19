// linefollower.ino - finale firmware (ESP32-S3, plan B).
//
// Opbouw:  lf_esp32 (hardware: hw.h, comms.h, opslag.h, board.h)
//          lf_core  (sensorverwerking + regeling, ook gebruikt door de simulatie)
// Compileren:
//   arduino-cli compile --fqbn esp32:esp32:esp32s3 --library ../../lib/lf_core --library ../../lib/lf_esp32 .
// Arduino IDE: Schets > Bibliotheek gebruiken > .ZIP-bibliotheek toevoegen > kies de map code/lib/lf_core,
// en daarna hetzelfde voor code/lib/lf_esp32.
//
// Typ "help" in de seriële monitor (115200) of in een TCP-terminal naar 192.168.4.1:23.
#include "board.h"
#include "lf_core.h"
#include "hw.h"
#include "comms.h"
#include "opslag.h"

enum Toestand { STIL, RIJDEN, KALIBREREN };
static Toestand toestand = STIL;
static lf::Regelaar regelaar;
static float refl[lf::N_SENSOR];
static lf::Uitgang laatste{};
static float vbat = 7.4f, v_links = 0, v_rechts = 0;
static uint32_t t_vorige = 0, cyclus_max_us = 0, n_cycli = 0;
static float t_kwijt = 0, t_laagbat = 0;
static char tekst[1200];

static const char *HELP =
  "commando's:\n"
  "  start | stop             rijden / stoppen (ook met de knop)\n"
  "  get [naam]               parameters tonen\n"
  "  set <naam> <waarde>      parameter zetten (bv. set kp 0.03, set debug on)\n"
  "  save | load | reset      bewaren in flash / terughalen / standaardwaarden\n"
  "  cal | cal stop           kalibreren: robot over de lijn heen en weer schuiven\n"
  "  calibrate white | black  kalibreren: alle sensoren op wit / op zwart\n"
  "  sensors                  ruwe en genormaliseerde sensorwaarden\n"
  "  status                   batterij, positie, snelheden, cyclustijd\n"
  "  motor <l|r> <duty> [ms]  motortest (duty -1..1, standaard 500 ms)\n";

static void start() {
  if (vbat < regelaar.p.vbat_min) { comms::schrijf("batterij te laag\n"); return; }
  regelaar.reset();
  regelaar.rijden = true;
  t_kwijt = 0;
  toestand = RIJDEN;
  comms::overal("START\n");
}

static void stop(const char *reden) {
  regelaar.rijden = false;
  toestand = STIL;
  hw::motoren(0, 0, false);
  snprintf(tekst, sizeof(tekst), "STOP (%s)\n", reden);
  comms::overal(tekst);
}

static void toon_sensoren() {
  lf::SensorUit s = regelaar.sensor.verwerk(refl, regelaar.p);
  int n = snprintf(tekst, sizeof(tekst), "aan  ");
  for (int i = 0; i < 8; i++) n += snprintf(tekst + n, sizeof(tekst) - n, "%5u", hw::adc_aan[i]);
  n += snprintf(tekst + n, sizeof(tekst) - n, "\nuit  ");
  for (int i = 0; i < 8; i++) n += snprintf(tekst + n, sizeof(tekst) - n, "%5u", hw::adc_uit[i]);
  n += snprintf(tekst + n, sizeof(tekst) - n, "\nrefl ");
  for (int i = 0; i < 8; i++) n += snprintf(tekst + n, sizeof(tekst) - n, "%5.0f", refl[i]);
  n += snprintf(tekst + n, sizeof(tekst) - n, "\nnorm ");
  for (int i = 0; i < 8; i++) n += snprintf(tekst + n, sizeof(tekst) - n, "%5.0f", s.norm[i]);
  snprintf(tekst + n, sizeof(tekst) - n, "\npositie %.1f mm  lijn %s%s\n", s.positie_mm, s.lijn ? "ja" : "NEE",
           s.kruispunt ? "  (kruispunt)" : "");
  comms::schrijf(tekst);
}

static void commando(char *regel) {
  char *w[6];
  int n = lf::splits(regel, w, 6);
  if (n == 0) return;
  if (lf::param_commando(regelaar.p, n, w, tekst, sizeof(tekst))) { comms::schrijf(tekst); return; }
  if (!strcmp(w[0], "help")) comms::schrijf(HELP);
  else if (!strcmp(w[0], "start")) start();
  else if (!strcmp(w[0], "stop")) stop("commando");
  else if (!strcmp(w[0], "debug")) { regelaar.p.debug = (n > 1 && !strcmp(w[1], "on")); comms::schrijf("ok\n"); }
  else if (!strcmp(w[0], "save")) { opslag::bewaar(regelaar.p, regelaar.sensor.kal); comms::schrijf("bewaard\n"); }
  else if (!strcmp(w[0], "load")) comms::schrijf(opslag::laad(regelaar.p, regelaar.sensor.kal) ? "geladen\n" : "niets bewaard\n");
  else if (!strcmp(w[0], "reset")) { regelaar.p = lf::Params(); regelaar.sensor.kal.standaard(); comms::schrijf("standaardwaarden (nog niet bewaard)\n"); }
  else if (!strcmp(w[0], "cal") && n > 1 && !strcmp(w[1], "stop")) { toestand = STIL; comms::schrijf("kalibratie klaar, 'save' om te bewaren\n"); }
  else if (!strcmp(w[0], "cal")) { stop("kalibreren"); regelaar.sensor.kal_start(); toestand = KALIBREREN;
                                   comms::schrijf("schuif de robot over de lijn, daarna 'cal stop'\n"); }
  else if (!strcmp(w[0], "calibrate") && n > 1 && !strcmp(w[1], "white")) { regelaar.sensor.kal_wit(refl); comms::schrijf("wit ok\n"); }
  else if (!strcmp(w[0], "calibrate") && n > 1 && !strcmp(w[1], "black")) { regelaar.sensor.kal_zwart(refl); comms::schrijf("zwart ok\n"); }
  else if (!strcmp(w[0], "sensors")) toon_sensoren();
  else if (!strcmp(w[0], "status")) {
    snprintf(tekst, sizeof(tekst), "vbat %.2f V | positie %.1f mm | v_links %.2f v_rechts %.2f m/s | "
             "encoders %d %d | cyclus max %lu us | toestand %d\n", vbat, laatste.positie_mm, v_links, v_rechts,
             hw::encoder_tellen(0), hw::encoder_tellen(1), (unsigned long)cyclus_max_us, toestand);
    cyclus_max_us = 0;
    comms::schrijf(tekst);
  }
  else if (!strcmp(w[0], "motor") && n >= 3) {
    if (toestand == RIJDEN) stop("motortest");
    float duty = atof(w[2]);
    int ms = n > 3 ? atoi(w[3]) : 500;
    bool links = w[1][0] == 'l';
    hw::motoren(links ? duty : 0, links ? 0 : duty, true);
    delay(constrain(ms, 0, 3000));
    hw::motoren(0, 0, false);
    snprintf(tekst, sizeof(tekst), "encoders na test: %d %d\n", hw::encoder_tellen(0), hw::encoder_tellen(1));
    comms::schrijf(tekst);
  }
  else { comms::schrijf("onbekend commando, typ 'help'\n"); }
}

void setup() {
  comms::init();
  hw::sensoren_init();
  hw::motoren_init();
  hw::encoders_init();
  hw::knop_init();
  if (!opslag::laad(regelaar.p, regelaar.sensor.kal)) Serial.println("geen bewaarde instellingen: standaardwaarden");
  hw::led(20, 0, 0);
  t_vorige = micros();
  Serial.println("linefollower klaar. Typ 'help'.");
}

void loop() {
  if (char *regel = comms::lees_regel()) commando(regel);
  if (hw::knop()) { if (toestand == RIJDEN) stop("knop"); else start(); }

  uint32_t nu = micros();
  if (nu - t_vorige < (uint32_t)regelaar.p.cyclus_us) return;
  float dt = (nu - t_vorige) * 1e-6f;
  t_vorige = nu;

  // --- elke cyclus: meten, regelen, sturen
  hw::sensoren_lees(refl, regelaar.p.led_diff > 0.5f);
  hw::encoders_snelheid(dt, v_links, v_rechts);
  if (++n_cycli % 20 == 0) vbat = hw::vbat_lees();

  if (toestand == KALIBREREN) { regelaar.sensor.kal_stap(refl); hw::led(0, 0, 30); }

  lf::Ingang in;
  memcpy(in.refl, refl, sizeof(refl));
  in.dt = dt; in.vbat = vbat; in.v_links = v_links; in.v_rechts = v_rechts;
  laatste = regelaar.stap(in);

  if (toestand == RIJDEN) {
    hw::motoren(laatste.duty_links, laatste.duty_rechts, true);
    t_kwijt = laatste.lijn ? 0 : t_kwijt + dt;
    if (t_kwijt > 0.5f) stop("lijn kwijt");
    t_laagbat = vbat < regelaar.p.vbat_min ? t_laagbat + dt : 0;
    if (t_laagbat > 1.0f) stop("batterij leeg");
    hw::led(0, 30, 0);
  } else if (toestand == STIL) {
    hw::motoren(0, 0, false);
    hw::led(vbat < regelaar.p.vbat_min ? 40 : 20, vbat < regelaar.p.vbat_min ? 20 : 0, 0);
  }

  // --- meetwaarden voor afstellen (elke 20 ms): t, positie, v_doel, v_links, v_rechts, duty L, duty R, vbat
  if (regelaar.p.debug > 0.5f && n_cycli % 20 == 0) {
    snprintf(tekst, sizeof(tekst), "%lu,%.1f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f\n", (unsigned long)millis(),
             laatste.positie_mm, laatste.v_doel, v_links, v_rechts, laatste.duty_links, laatste.duty_rechts, vbat);
    comms::overal(tekst);
  }
  uint32_t duur = micros() - nu;
  if (duur > cyclus_max_us) cyclus_max_us = duur;
}
