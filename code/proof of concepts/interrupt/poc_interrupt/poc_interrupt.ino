// PoC start/stop: drukknop via hardware-interrupt, met debounce (ontdendering).
// Knop tussen GPIO21 en GND, interne pull-up. Ingebouwde RGB-led van de devkit toont de toestand.
#include "board.h"

volatile bool rijden = false;
volatile uint32_t laatsteDruk = 0;

void IRAM_ATTR knopISR() {
  uint32_t nu = millis();
  if (nu - laatsteDruk > 200) {   // 200 ms ontdendering
    rijden = !rijden;
    laatsteDruk = nu;
  }
}

void setup() {
  Serial.begin(115200);
  pinMode(PIN_BTN, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(PIN_BTN), knopISR, FALLING);
}

void loop() {
  static bool vorige = !rijden;
  if (rijden != vorige) {
    vorige = rijden;
    Serial.println(rijden ? "START" : "STOP");
#ifdef RGB_BUILTIN
    rgbLedWrite(RGB_BUILTIN, rijden ? 0 : 40, rijden ? 40 : 0, 0);  // groen = rijden, rood = stop
#endif
  }
  delay(5);
}
