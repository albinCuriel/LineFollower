// board.h - hardwarelaag linefollower (ESP32-S3 devkit N8R2, plan B gaatjesprint)
// Pinverdeling = KiCad-schema "technische tekeningen/elektronisch/kicad" + bedradingslijst.md.
// Wissel je ooit naar het backupbord (ATmega32U4), dan verandert enkel dit bestand.
#pragma once
#include <Arduino.h>

// --- QTR-8A sensorarray (ADC1, werkt ook met wifi aan) ---
static const uint8_t PIN_SENSOR[8] = {1, 2, 3, 4, 5, 6, 7, 8};
static const uint8_t PIN_LEDON     = 11;   // IR-leds van de QTR aan/uit

// --- Batterijmeting: deler 100k / 33k ---
static const uint8_t PIN_VBAT      = 9;
static const float   VBAT_DELER    = (100.0f + 33.0f) / 33.0f;  // 8,4 V -> 2,08 V

// --- TB6612FNG ---
static const uint8_t PIN_PWMA = 12, PIN_AIN1 = 13, PIN_AIN2 = 14;   // motor links
static const uint8_t PIN_PWMB = 15, PIN_BIN1 = 16, PIN_BIN2 = 17;   // motor rechts
static const uint8_t PIN_STBY = 18;                                 // laag = motoren uit
static const uint32_t PWM_FREQ = 20000;  // 20 kHz: niet hoorbaar
static const uint8_t  PWM_BITS = 10;     // 0..1023
static const int      PWM_MAX  = (1 << PWM_BITS) - 1;

// --- Encoders (Hall, 7 PPR op de motoras) ---
static const uint8_t PIN_ENC_L_A = 39, PIN_ENC_L_B = 40;
static const uint8_t PIN_ENC_R_A = 41, PIN_ENC_R_B = 42;

// --- Bediening en weergave ---
static const uint8_t PIN_BTN = 21;   // start/stop naar GND, interne pull-up
static const uint8_t PIN_RGB = 47;   // WS2812 8 leds (DIN)
static const uint8_t RGB_AANTAL = 8;
