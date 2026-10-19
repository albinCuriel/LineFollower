# Proof of Concepts

Een proof of concept is een combinatie van minimale hard- en software om eenvoudig aan te tonen dat iets werkt.  
Proof of concepts kunnen enerzijds als eerste poging dienen om een bepaald onderdeel van het project werkend te krijgen. Anderzijds kunnen ze tijdens het debuggen van het finale project dienen als test om eventuele hardware problemen te elimineren bij onduidelijke problemen.
<br />  
<br />
Een proof of concept bestaat uit
* een elektronisch schema (indien van toepassing)
* minimale code om de voorop gestelde zaken te demonstreren
* minimale uitleg / aandachtspunten
<br />
De elektronische schakelingen van de proof of concepts komen bij voorkeur overeen met deze van de uiteindelijke linefollower, zodat de code zonder aanpassingen op het finale project kan draaien.

| Proof of concept | Test | Sketch |
|---|---|---|
| [sensor](sensor/readme.md) | 8 sensoren apart uitlezen, met en zonder IR-licht | `sensor/poc_sensor` |
| [H-brug](hbridge/readme.md) | 2 motoren traploos, beide richtingen | `hbridge/poc_hbridge` |
| [start/stop-interrupt](interrupt/readme.md) | drukknop via interrupt met ontdendering | `interrupt/poc_interrupt` |
| [draadloze communicatie](wireless%20communication/readme.md) | duplex tussen robot en gsm via wifi | `wireless communication/poc_wifi` |

Alle sketches compileren voor de ESP32-S3 (`esp32:esp32:esp32s3`) en gebruiken dezelfde pinnen als de robot (`board.h`). Ze draaien dus zonder aanpassing op de afgewerkte robot.
