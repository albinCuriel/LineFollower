# Gebruiksaanwijzing

### opladen / vervangen batterijen
- De robot rijdt op een **LiPo 2S 450 mAh** met XT30-stekker, vast met klittenband boven de wielas.
- Wisselen: robot uit (SW1), XT30 lostrekken (aan de stekker, niet aan de draden), andere batterij aansluiten. Er is een reservebatterij.
- Opladen met de **Imax B3**: steek **enkel de witte balansstekker** (JST-XH, 3 pinnen) in de 2S-aansluiting van de lader. De lader balanceert zelf (±1 A, ±30 min vanaf leeg).
- Laad op in de **LiPo-bag**, op een onbrandbare ondergrond, en nooit zonder toezicht.
- Spanning: vol = 8,4 V, nominaal 7,4 V. **Stop met rijden onder 6,6 V** (de robot meet dit zelf via GPIO9). Onder 6,0 V raakt de batterij beschadigd.
- Een opgezwollen of beschadigde batterij niet meer gebruiken of laden.

### draadloze communicatie
#### verbinding maken
1. Zet de robot aan (SW1).
2. Verbind je gsm of laptop met het wifinetwerk **linefollower**. Het wachtwoord staat in de code (`WIFI_WACHTWOORD`).
3. Open een raw-TCP-terminal naar **192.168.4.1**, poort **23**:
   - Android: app "Serial WiFi Terminal"
   - laptop: PuTTY, verbindingstype "Raw"
4. Typ een commando en druk op enter. Het antwoord verschijnt in de terminal.

#### commando's
debug [on/off]  
start  
stop  
set cycle [µs]  
set kp / ki / kd [waarde]  
set vbocht / vrecht [m/s]  
get (alle parameters met uitleg)  
save / load / reset  
cal ... cal stop  
calibrate black  
calibrate white  
sensors / status  
motor l|r [duty] [ms]  

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
De robot rijdt stabiel met volgende parameters:  
(in te vullen na het afstellen op het parcours)

### start/stop button
- De start/stop-knop zit aan de **linkerrand**, ter hoogte van de ESP32.
- Eén druk = start, nog een druk = stop. De ingebouwde RGB-led toont de toestand: **groen = rijden, rood = stil**.
- De aan/uit-schakelaar **SW1** zit links achteraan, naast de batterijstekker. De power-led brandt als de robot aan staat.
