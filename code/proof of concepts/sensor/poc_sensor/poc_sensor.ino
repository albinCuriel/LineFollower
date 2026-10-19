// PoC sensor: 8 QTR-8A-sensoren onafhankelijk uitlezen (geen kalibratie/normalisatie).
// Per sensor 2 metingen: IR-leds aan en uit. Verschil = reflectie zonder omgevingslicht.
// Volledig ADC-bereik: 12 bit, 11 dB demping (0..~3,1 V), zelfde voeding als de QTR (3,3 V).
#include "board.h"

void setup() {
  Serial.begin(115200);
  pinMode(PIN_LEDON, OUTPUT);
  analogReadResolution(12);
  analogSetAttenuation(ADC_11db);
}

void leesAlles(uint16_t *waarden) {
  for (int i = 0; i < 8; i++) waarden[i] = analogRead(PIN_SENSOR[i]);
}

void loop() {
  uint16_t aan[8], uit[8];
  digitalWrite(PIN_LEDON, HIGH); delayMicroseconds(200); leesAlles(aan);
  digitalWrite(PIN_LEDON, LOW);  delayMicroseconds(200); leesAlles(uit);

  // QTR: meer reflectie (wit) = lagere spanning. Zwart = hoog.
  for (int i = 0; i < 8; i++) {
    int verschil = (int)uit[i] - (int)aan[i];
    Serial.printf("S%d:%4d/%4d(%5d)  ", i + 1, aan[i], uit[i], verschil);
  }
  Serial.println();
  delay(100);
}
