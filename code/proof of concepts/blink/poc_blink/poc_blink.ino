// poc_blink.ino - het eenvoudigste programma: de ingebouwde RGB-led knippert 1x per seconde.
// Toont aan dat de programmeeromgeving, de drivers en het uploaden werken, dat de microcontroller
// leeft en dat de klok klopt (tel 10 keer knipperen = 10 seconden).
// Niet-blokkerend (millis), zodat hetzelfde patroon in de andere programma's bruikbaar is.
#include "board.h"

static uint32_t t_vorige = 0;
static bool aan = false;
static uint32_t teller = 0;

void setup() {
  Serial.begin(115200);
  Serial.println("poc_blink: de led knippert 1 Hz (0,5 s aan, 0,5 s uit)");
}

void loop() {
  uint32_t nu = millis();
  if (nu - t_vorige >= 500) {
    t_vorige = nu;
    aan = !aan;
    rgbLedWrite(PIN_RGB, 0, 0, aan ? 30 : 0);   // blauw
    if (aan) { Serial.print("blink "); Serial.println(++teller); }
  }
}
