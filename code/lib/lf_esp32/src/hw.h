// hw.h - hardwarelaag ESP32-S3: sensoren, motoren, encoders (PCNT), batterij, knop, statusled.
// Alles wat van het bord afhangt staat hier en in board.h. De regeling zelf zit in lf_core.
#pragma once
#include <Arduino.h>
#include "driver/pulse_cnt.h"
#include "board.h"
#include "lf_core.h"

namespace hw {

// ---------------------------------------------------------------- sensoren (QTR-8A)
// Meet elke sensor met de IR-leds UIT en AAN. reflectie = uit - aan (hoog = wit), omgevingslicht valt weg.
static uint16_t adc_aan[lf::N_SENSOR], adc_uit[lf::N_SENSOR];

inline void sensoren_init() {
  analogReadResolution(12);
  analogSetAttenuation(ADC_11db);          // volledig bereik 0..~3,1 V
  pinMode(PIN_LEDON, OUTPUT);
  digitalWrite(PIN_LEDON, HIGH);
}

inline void sensoren_lees(float refl[lf::N_SENSOR], bool led_diff) {
  if (led_diff) {
    digitalWrite(PIN_LEDON, LOW);
    delayMicroseconds(80);                 // fototransistor laten uitzwingen
    for (int i = 0; i < lf::N_SENSOR; i++) adc_uit[i] = analogRead(PIN_SENSOR[i]);
    digitalWrite(PIN_LEDON, HIGH);
    delayMicroseconds(80);
  }
  for (int i = 0; i < lf::N_SENSOR; i++) adc_aan[i] = analogRead(PIN_SENSOR[i]);
  for (int i = 0; i < lf::N_SENSOR; i++)
    refl[i] = lf::Sensor::reflectie(adc_aan[i], led_diff ? adc_uit[i] : 4095, led_diff);
}

// ---------------------------------------------------------------- motoren (TB6612FNG)
inline void motoren_init() {
  for (uint8_t p : {PIN_AIN1, PIN_AIN2, PIN_BIN1, PIN_BIN2, PIN_STBY}) { pinMode(p, OUTPUT); digitalWrite(p, LOW); }
  ledcAttach(PIN_PWMA, PWM_FREQ, PWM_BITS);
  ledcAttach(PIN_PWMB, PWM_FREQ, PWM_BITS);
}

inline void motor(uint8_t pwm, uint8_t in1, uint8_t in2, float duty) {   // duty -1..1
  duty = constrain(duty, -1.0f, 1.0f);
  digitalWrite(in1, duty > 0);
  digitalWrite(in2, duty < 0);
  ledcWrite(pwm, (uint32_t)(fabsf(duty) * PWM_MAX));
}

inline void motoren(float links, float rechts, bool aan) {
  digitalWrite(PIN_STBY, aan);
  motor(PIN_PWMA, PIN_AIN1, PIN_AIN2, aan ? links : 0);
  motor(PIN_PWMB, PIN_BIN1, PIN_BIN2, aan ? rechts : 0);
}

// ---------------------------------------------------------------- encoders (hardware-teller PCNT, kwadratuur x4)
static pcnt_unit_handle_t enc_unit[2];
static const int ENC_VENSTER = 10;          // snelheid over 10 cycli (zoals in de simulatie)
static int enc_hist[2][ENC_VENSTER + 1];
static int enc_idx = 0;

inline void encoder_maak(int i, uint8_t a, uint8_t b, bool omkeren) {
  pinMode(a, INPUT_PULLUP); pinMode(b, INPUT_PULLUP);
  pcnt_unit_config_t ucfg = {};
  ucfg.low_limit = -30000; ucfg.high_limit = 30000;
  ucfg.flags.accum_count = 1;               // telt door voorbij de grenzen
  pcnt_new_unit(&ucfg, &enc_unit[i]);
  pcnt_glitch_filter_config_t f = {.max_glitch_ns = 1000};
  pcnt_unit_set_glitch_filter(enc_unit[i], &f);
  pcnt_chan_config_t ca = {}; ca.edge_gpio_num = a; ca.level_gpio_num = b;
  pcnt_chan_config_t cb = {}; cb.edge_gpio_num = b; cb.level_gpio_num = a;
  pcnt_channel_handle_t cha, chb;
  pcnt_new_channel(enc_unit[i], &ca, &cha);
  pcnt_new_channel(enc_unit[i], &cb, &chb);
  auto op = omkeren ? PCNT_CHANNEL_EDGE_ACTION_INCREASE : PCNT_CHANNEL_EDGE_ACTION_DECREASE;
  auto neer = omkeren ? PCNT_CHANNEL_EDGE_ACTION_DECREASE : PCNT_CHANNEL_EDGE_ACTION_INCREASE;
  pcnt_channel_set_edge_action(cha, op, neer);
  pcnt_channel_set_level_action(cha, PCNT_CHANNEL_LEVEL_ACTION_KEEP, PCNT_CHANNEL_LEVEL_ACTION_INVERSE);
  pcnt_channel_set_edge_action(chb, neer, op);
  pcnt_channel_set_level_action(chb, PCNT_CHANNEL_LEVEL_ACTION_KEEP, PCNT_CHANNEL_LEVEL_ACTION_INVERSE);
  pcnt_unit_add_watch_point(enc_unit[i], ucfg.low_limit);
  pcnt_unit_add_watch_point(enc_unit[i], ucfg.high_limit);
  pcnt_unit_enable(enc_unit[i]);
  pcnt_unit_clear_count(enc_unit[i]);
  pcnt_unit_start(enc_unit[i]);
}

inline void encoders_init() {
  encoder_maak(0, PIN_ENC_L_A, PIN_ENC_L_B, false);
  encoder_maak(1, PIN_ENC_R_A, PIN_ENC_R_B, true);   // rechter motor staat gespiegeld
}

inline int encoder_tellen(int i) { int c = 0; pcnt_unit_get_count(enc_unit[i], &c); return c; }

// Roep elke cyclus 1x aan. Geeft wielsnelheden in m/s (gemiddeld over ENC_VENSTER cycli).
inline void encoders_snelheid(float dt, float &v_links, float &v_rechts) {
  enc_idx = (enc_idx + 1) % (ENC_VENSTER + 1);
  float v[2];
  for (int i = 0; i < 2; i++) {
    enc_hist[i][enc_idx] = encoder_tellen(i);
    int oud = enc_hist[i][(enc_idx + 1) % (ENC_VENSTER + 1)];
    v[i] = (enc_hist[i][enc_idx] - oud) * (PI * lf::WIEL_D_M / lf::TELLEN_PER_TOER) / (dt * ENC_VENSTER);
  }
  v_links = v[0]; v_rechts = v[1];
}

// ---------------------------------------------------------------- batterij
static float vbat_filter = 7.4f;
inline float vbat_lees() {
  float v = analogReadMilliVolts(PIN_VBAT) / 1000.0f * VBAT_DELER;
  vbat_filter += 0.05f * (v - vbat_filter);
  return vbat_filter;
}

// ---------------------------------------------------------------- start/stop-knop (interrupt)
static volatile bool knop_gedrukt = false;
static volatile uint32_t knop_tijd = 0;
static void IRAM_ATTR knop_isr() {   // niet 'inline': IRAM-functies mogen niet inline (linkerfout)
  uint32_t nu = millis();
  if (nu - knop_tijd > 200) { knop_gedrukt = true; knop_tijd = nu; }   // ontdendering 200 ms
}
inline void knop_init() {
  pinMode(PIN_BTN, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(PIN_BTN), knop_isr, FALLING);
}
inline bool knop() { bool k = knop_gedrukt; knop_gedrukt = false; return k; }

// ---------------------------------------------------------------- statusled (ingebouwde RGB)
inline void led(uint8_t r, uint8_t g, uint8_t b) { rgbLedWrite(PIN_RGB, r, g, b); }

}  // namespace hw
