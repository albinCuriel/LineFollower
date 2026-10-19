// basis.ino - basisprogramma volgens de cursus (ESP32-S3).
//
// Werkt samen:
//  - instelbare parameters via commando's (USB of wifi): cyclustijd, debug, start/stop
//  - parameters bewaard in het flashgeheugen (de "EEPROM" van de ESP32)
//  - start/stop ook met de drukknop via een externe interrupt
//  - draadloze communicatie: eigen wifinetwerk "linefollower", TCP-terminal naar 192.168.4.1:23
// Met de cyclus knippert de statusled: elke cyclus wisselt hij (cycle 500000 = 1 Hz).
//
// Compileren: arduino-cli compile --fqbn esp32:esp32:esp32s3 --library ../../lib/lf_core --library ../../lib/lf_esp32 .
#include "lf_core.h"
#include "board.h"
#include "hw.h"
#include "comms.h"
#include "opslag.h"

static lf::Params p;
static lf::Kalibratie kal;   // niet gebruikt in het basisprogramma, wel mee bewaard
static bool rijden = false, led_aan = false;
static uint32_t t_vorige = 0, n = 0;
static char tekst[1200];

static void zet_rijden(bool r) {
  rijden = r;
  comms::overal(rijden ? "START\n" : "STOP\n");
}

static void commando(char *regel) {
  char *w[4];
  int k = lf::splits(regel, w, 4);
  if (k == 0) return;
  if (!strcmp(w[0], "get") || !strcmp(w[0], "set")) {
    if (k >= 2 && strcmp(w[1], "cycle") && strcmp(w[1], "debug")) {
      comms::schrijf("basisprogramma: enkel 'cycle' en 'debug'\n"); return;
    }
    lf::param_commando(p, k, w, tekst, sizeof(tekst));
    comms::schrijf(tekst);
  }
  else if (!strcmp(w[0], "debug")) { p.debug = k > 1 && !strcmp(w[1], "on"); comms::schrijf("ok\n"); }
  else if (!strcmp(w[0], "start")) zet_rijden(true);
  else if (!strcmp(w[0], "stop")) zet_rijden(false);
  else if (!strcmp(w[0], "save")) { opslag::bewaar(p, kal); comms::schrijf("bewaard in flash\n"); }
  else comms::schrijf("commando's: set cycle <us> | set debug on|off | debug on|off | start | stop | save | get\n");
}

void setup() {
  comms::init();
  hw::knop_init();
  kal.standaard();
  if (opslag::laad(p, kal)) Serial.println("instellingen geladen uit flash");
  t_vorige = micros();
}

void loop() {
  if (char *r = comms::lees_regel()) commando(r);
  if (hw::knop()) zet_rijden(!rijden);                 // interrupt heeft de knop gezien

  uint32_t nu = micros();
  if (nu - t_vorige < (uint32_t)p.cyclus_us) return;
  t_vorige = nu;
  n++;
  led_aan = !led_aan;                                   // knipperen op het ritme van de cyclus
  hw::led(0, led_aan ? (rijden ? 30 : 0) : 0, led_aan ? (rijden ? 0 : 30) : 0);   // groen = rijden, blauw = stil
  if (p.debug > 0.5f) {
    snprintf(tekst, sizeof(tekst), "cyclus %lu  rijden %d  t=%lu ms\n", (unsigned long)n, rijden, (unsigned long)millis());
    comms::overal(tekst);
  }
}
