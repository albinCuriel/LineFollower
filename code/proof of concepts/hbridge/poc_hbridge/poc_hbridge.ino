// PoC H-brug: 2 motoren onafhankelijk en traploos regelen in snelheid en draairichting.
// Zet de robot op de testbok (wielen in de lucht)! Volgorde: links vooruit/achteruit, rechts idem, samen.
#include "board.h"

void motor(uint8_t pwmPin, uint8_t in1, uint8_t in2, int snelheid) {  // -PWM_MAX .. +PWM_MAX
  snelheid = constrain(snelheid, -PWM_MAX, PWM_MAX);
  digitalWrite(in1, snelheid > 0);
  digitalWrite(in2, snelheid < 0);
  ledcWrite(pwmPin, abs(snelheid));
}
void links(int s)  { motor(PIN_PWMA, PIN_AIN1, PIN_AIN2, s); }
void rechts(int s) { motor(PIN_PWMB, PIN_BIN1, PIN_BIN2, s); }

void ramp(void (*m)(int), int doel) {
  for (int s = 0; abs(s) <= abs(doel); s += (doel > 0 ? 8 : -8)) { m(s); delay(10); }
  for (int s = doel; s != 0; s -= (doel > 0 ? 8 : -8)) { m(s); delay(10); }
  m(0); delay(300);
}

void setup() {
  Serial.begin(115200);
  for (uint8_t p : {PIN_AIN1, PIN_AIN2, PIN_BIN1, PIN_BIN2, PIN_STBY}) pinMode(p, OUTPUT);
  ledcAttach(PIN_PWMA, PWM_FREQ, PWM_BITS);
  ledcAttach(PIN_PWMB, PWM_FREQ, PWM_BITS);
  digitalWrite(PIN_STBY, HIGH);
}

void loop() {
  const int max = PWM_MAX * 70 / 100;  // 6V-motoren op 7,4-8,4 V: max 70 %
  Serial.println("links vooruit/achteruit");  ramp(links, max);  ramp(links, -max);
  Serial.println("rechts vooruit/achteruit"); ramp(rechts, max); ramp(rechts, -max);
  Serial.println("samen, tegengesteld");
  links(max / 2); rechts(-max / 2); delay(1000); links(0); rechts(0);
  delay(1500);
}
