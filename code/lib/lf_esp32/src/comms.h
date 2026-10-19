// comms.h - commando's via USB (Serial) en wifi (eigen netwerk + TCP-poort 23).
// Beide kanalen werken tegelijk en gebruiken dezelfde commando's. Antwoorden gaan naar het kanaal
// waar het commando vandaan kwam; meetwaarden (debug) gaan naar beide.
#pragma once
#include <Arduino.h>
#include <WiFi.h>

namespace comms {

static const char *WIFI_NAAM = "linefollower";
static const char *WIFI_WACHTWOORD = "verander-mij";   // min. 8 tekens: AANPASSEN voor gebruik
static WiFiServer server(23);
static WiFiClient client;
static char buf_s[96], buf_w[96];
static int len_s = 0, len_w = 0;
static Print *antwoord = &Serial;    // kanaal van het laatste commando

inline void init() {
  Serial.begin(115200);
  WiFi.mode(WIFI_AP);
  WiFi.softAP(WIFI_NAAM, WIFI_WACHTWOORD);
  server.begin();
  server.setNoDelay(true);
}

inline void schrijf(const char *tekst) {   // naar het kanaal van het laatste commando
  antwoord->print(tekst);
}

inline void overal(const char *tekst) {    // naar USB en wifi
  Serial.print(tekst);
  if (client && client.connected()) client.print(tekst);
}

// Leest tekens; geeft een volledige regel terug (of nullptr). Niet-blokkerend.
inline char *lees_regel() {
  if (server.hasClient()) {
    if (client) client.stop();
    client = server.accept();
    client.println("linefollower: verbonden. Typ 'help'.");
  }
  while (Serial.available()) {
    char c = Serial.read();
    if (c == '\n' || c == '\r') { if (len_s) { buf_s[len_s] = 0; len_s = 0; antwoord = &Serial; return buf_s; } }
    else if (len_s < (int)sizeof(buf_s) - 1) buf_s[len_s++] = c;
  }
  while (client && client.connected() && client.available()) {
    char c = client.read();
    if (c == '\n' || c == '\r') { if (len_w) { buf_w[len_w] = 0; len_w = 0; antwoord = &client; return buf_w; } }
    else if (len_w < (int)sizeof(buf_w) - 1) buf_w[len_w++] = c;
  }
  return nullptr;
}

}  // namespace comms
