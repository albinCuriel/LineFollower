// PoC draadloze communicatie: duplex tussen ESP32-S3 en laptop/smartphone via wifi.
// De robot maakt zijn eigen netwerk "linefollower" (wachtwoord in WIFI_WACHTWOORD).
// Verbind en open een raw-TCP-terminal naar 192.168.4.1 poort 23 (PuTTY "Raw", of de
// Android-app "Serial WiFi Terminal"). Alles wat je typt komt op de USB-monitor en omgekeerd.
#include <WiFi.h>
#include "board.h"

const char *WIFI_NAAM = "linefollower";
const char *WIFI_WACHTWOORD = "verander-mij";   // min. 8 tekens, pas aan voor gebruik
WiFiServer server(23);
WiFiClient client;

void setup() {
  Serial.begin(115200);
  WiFi.softAP(WIFI_NAAM, WIFI_WACHTWOORD);
  server.begin();
  Serial.printf("AP actief, verbind en ga naar %s:23\n", WiFi.softAPIP().toString().c_str());
}

void loop() {
  if (!client || !client.connected()) {
    WiFiClient nieuw = server.accept();
    if (nieuw) { client = nieuw; client.println("linefollower: verbonden"); Serial.println("client verbonden"); }
  }
  while (client && client.available()) {           // wifi -> robot
    String regel = client.readStringUntil('\n'); regel.trim();
    Serial.printf("ontvangen: %s\n", regel.c_str());
    client.printf("echo: %s\n", regel.c_str());     // robot -> wifi (duplex)
  }
  while (Serial.available() && client) client.write(Serial.read());  // USB -> wifi
}
