# Gebruiksaanwijzing

### opladen / vervangen batterijen
- De robot rijdt op een **LiPo 2S 450 mAh** met XT30-stekker, vast met klittenband boven de wielas.
- Wisselen: robot uit (SW1), XT30 lostrekken (aan de stekker, niet aan de draden), andere batterij aansluiten. Er is een reservebatterij.
- Opladen met de **Imax B3**: steek **enkel de witte balansstekker** (JST-XH, 3 pinnen) in de 2S-aansluiting van de lader. De lader balanceert zelf (±1 A, ±30 min vanaf leeg).
- Laad op in de **LiPo-bag**, op een onbrandbare ondergrond, en nooit zonder toezicht.
- Spanning: vol = 8,4 V, nominaal 7,4 V. **Stop met rijden onder 6,6 V** (de robot meet dit zelf via GPIO9). Onder 6,0 V raakt de batterij beschadigd.
- Een opgezwollen of beschadigde batterij niet meer gebruiken of laden.

### USB en batterij: nooit tegelijk
De buck voedt de ESP32 via de 3V3-pin. Zit de USB-kabel erin terwijl de robot aan staat (SW1), dan voeden twee bronnen dezelfde 3,3 V-lijn en kan het devkit of de buck stuk gaan.
- Code uploaden of de seriële monitor gebruiken via USB: **SW1 uit**.
- Testen met de motoren aan: gebruik de wifi-terminal (hieronder), of een USB-kabel waarvan de rode draad (5 V) doorgeknipt is.

### draadloze communicatie
#### verbinding maken
1. Zet de robot aan (SW1).
2. Verbind je gsm of laptop met het wifinetwerk **linefollower**. Wachtwoord: **lijnvolger2026** (staat in [comms.h](../code/lib/lf_esp32/src/comms.h) als `WIFI_WACHTWOORD`; verander het daar als je wil).
3. Open een raw-TCP-terminal naar **192.168.4.1**, poort **23**:
   - Android: app "Serial WiFi Terminal"
   - laptop: PuTTY, verbindingstype "Raw"
4. Typ een commando en druk op enter. Het antwoord verschijnt in de terminal.

#### commando's
debug [on/off] (meetwaarden doorsturen); `debug` alleen = cyclustijd + rekentijd  
start  
stop  
set cycle [µs]  
set kp / ki / kd [waarde]  
set vbocht / vrecht [m/s]  
get (alle parameters met uitleg)  
save / load / reset (elke `set` wordt ook automatisch bewaard)  
cal ... cal stop  
calibrate black  
calibrate white  
sensors / status  
motor l|r [duty] [ms]  
invert sensor|motorl|motorr|encl|encr (richting omkeren zonder solderen)  
help  

Volledige lijst met uitleg: [code/finaal](../code/finaal/readme.md). Alle parameters: typ `get`.

### kalibratie
Snelste manier: typ `cal`, schuif de robot een paar keer met de hand dwars over de lijn (alle sensoren moeten wit én zwart zien) en typ `cal stop`, dan `save`. De led brandt blauw tijdens het kalibreren.

Of per kleur:
1. Zet de robot met alle sensoren op het **witte** vlak en stuur `calibrate white`.
2. Zet de robot met alle sensoren op de **zwarte** lijn en stuur `calibrate black`.
3. Typ `save`: dan blijft de kalibratie bewaard na uitschakelen. Herhaal dit bij ander licht of een andere ondergrond.

### settings
Startwaarden uit de [simulatie](../simulatie/resultaat_tune.md) (staan al als standaard in de firmware).
Begin trager: `set vbocht 0.4` en `set vrecht 0.6`, en verhoog stap voor stap.
De robot rijdt stabiel met volgende parameters (resultaat van de simulatie op parcours 3, staan als standaard in de firmware; worden bijgesteld na de testritten):

| Parameter | Commando | Waarde | Betekenis |
|---|---|---|---|
| cyclustijd | `set cycle` | 1000 µs | regelcyclus 1 kHz |
| P | `set kp` | 0.0267 | m/s stuurcorrectie per mm afwijking |
| I | `set ki` | 0.0214 | wegwerken blijvende afwijking |
| D | `set kd` | 0.00145 | demping (m/s per mm/s) |
| snelheid bocht | `set vbocht` | 0.74 m/s | |
| snelheid rechtdoor | `set vrecht` | 2.1 m/s | boost op rechte stukken |
| P wielsnelheid | `set kpv` | 0.6 | snelheidsregeling per wiel (encoders) |
| I wielsnelheid | `set kiv` | 8.0 | |

Eerste ritten: `set vbocht 0.4` en `set vrecht 0.6`, daarna stap voor stap naar de waarden hierboven. Verwachte gemiddelde snelheid met deze waarden: ±0,82 m/s (simulatie, 90 % marge). Typ `save` om te bewaren.

### start/stop button
- De start/stop-knop zit aan de **linkerrand**, ter hoogte van de ESP32.
- Eén druk = start, nog een druk = stop. De ingebouwde RGB-led toont de toestand: **groen = rijden, rood = stil**.
- De aan/uit-schakelaar **SW1** zit links achteraan, naast de batterijstekker. De power-led brandt als de robot aan staat.
