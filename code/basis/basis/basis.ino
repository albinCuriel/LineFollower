// basis.ino - basisprogramma volgens de cursus (ESP32-S3).
//
// Werkt samen (zie het leerpad "basis programma"):
//  - SerialCommand: commando's inlezen zonder de loop te blokkeren (USB en wifi)
//      set cycle <us> | set debug on|off | debug | start | stop | get | save
//  - EEPROM: de parameters staan in een struct en worden bij elke wijziging bewaard in het
//    flashgeheugen (NVS, de "EEPROM" van de ESP32). Bij het opstarten worden ze teruggelezen.
//  - cyclus: het cyclische deel loopt op een vaste, instelbare cyclustijd. De rekentijd per cyclus
//    wordt gemeten; 'debug' toont de cyclustijd en de langste rekentijd sinds de vorige 'debug'.
//  - start/stop met een commando of met de drukknop via een externe interrupt.
//  - draadloze communicatie: eigen wifinetwerk "linefollower", TCP-terminal naar 192.168.4.1:23.
// In het cyclische deel wordt NIET naar de seriele poort geschreven. De statusled wisselt elke
// cyclus (set cycle 500000 = 1 Hz knipperen): groen = gestart, blauw = gestopt.
//
// Compileren: arduino-cli compile --fqbn esp32:esp32:esp32s3 --library ../../lib/lf_core --library ../../lib/lf_esp32 .
#include "lf_core.h"
#include "board.h"
#include "hw.h"
#include "comms.h"
#include "opslag.h"

static lf::Params p;         // alle instelbare parameters in 1 struct (cyclus_us, debug, ...)
static lf::Kalibratie kal;   // niet gebruikt in het basisprogramma, wel mee bewaard
static bool rijden = false, led_aan = false;
static uint32_t t_vorige = 0, t_debug = 0, n_cycli = 0;
static uint32_t rekentijd_max_us = 0;   // langste rekentijd van het cyclische deel
static char tekst[1200];

static void zet_rijden(bool r) {
  rijden = r;
  comms::overal(rijden ? "START\n" : "STOP\n");
}

// --- eventhandlers: alle in- en uitvoer naar de gebruiker gebeurt hier, niet in het cyclische deel
static void onSet(int k, char *w[]) {
  if (k >= 2 && strcmp(w[1], "cycle") && strcmp(w[1], "debug")) {
    comms::schrijf("basisprogramma: enkel 'cycle' en 'debug'\n");
    return;
  }
  lf::param_commando(p, k, w, tekst, sizeof(tekst));
  comms::schrijf(tekst);
  if (!strcmp(w[0], "set")) opslag::bewaar(p, kal);   // EEPROM: bij elke wijziging bewaren
}

static void onDebug() {
  snprintf(tekst, sizeof(tekst), "cycle time: %lu us\ncalculation time (max): %lu us\ndebug: %s\nrunning: %s\n",
           (unsigned long)p.cyclus_us, (unsigned long)rekentijd_max_us, p.debug > 0.5f ? "on" : "off",
           rijden ? "yes" : "no");
  rekentijd_max_us = 0;
  comms::schrijf(tekst);
}

static void onUnknown() {
  comms::schrijf("unknown command. Gebruik: set cycle <us> | set debug on|off | debug | start | stop | get | save\n");
}

static void commando(char *regel) {
  char *w[4];
  int k = lf::splits(regel, w, 4);
  if (k == 0) return;
  if (!strcmp(w[0], "set") || !strcmp(w[0], "get")) onSet(k, w);
  else if (!strcmp(w[0], "debug")) onDebug();
  else if (!strcmp(w[0], "start")) zet_rijden(true);
  else if (!strcmp(w[0], "stop")) zet_rijden(false);
  else if (!strcmp(w[0], "save")) { opslag::bewaar(p, kal); comms::schrijf("bewaard in flash\n"); }
  else onUnknown();
}

void setup() {
  comms::init();
  hw::knop_init();
  kal.standaard();
  if (opslag::laad(p, kal)) Serial.println("instellingen geladen uit flash");
  t_vorige = micros();
}

void loop() {
  // --- niet-cyclisch deel: commando's en de knop (niet-blokkerend)
  if (char *r = comms::lees_regel()) commando(r);
  if (hw::knop()) zet_rijden(!rijden);                 // de interrupt heeft de knop gezien

  if (p.debug > 0.5f && millis() - t_debug >= 1000) {  // debugvlag: 1x per seconde een bericht (non-blocking wait)
    t_debug = millis();
    snprintf(tekst, sizeof(tekst), "debug: %lu cycli, rijden %d\n", (unsigned long)n_cycli, rijden);
    comms::overal(tekst);
  }

  // --- cyclisch deel: exact om de p.cyclus_us microseconden
  uint32_t nu = micros();
  if (nu - t_vorige < (uint32_t)p.cyclus_us) return;
  t_vorige = nu;
  n_cycli++;
  led_aan = !led_aan;                                   // knipperen op het ritme van de cyclus
  hw::led(0, (led_aan && rijden) ? 30 : 0, (led_aan && !rijden) ? 30 : 0);   // groen = gestart, blauw = gestopt
  // (in de finale code komt hier: sensoren lezen -> PID -> motoren)

  uint32_t rekentijd = micros() - nu;
  if (rekentijd > rekentijd_max_us) rekentijd_max_us = rekentijd;
}
