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
set power [0..255]  
set diff [0..1]  
set kp [0..]  
set ki [0..]  
set kd [0..]  
calibrate black  
calibrate white  

(definitieve lijst volgt met het [basisprogramma](../code/basis/readme.md))

### kalibratie
1. Zet de robot met alle sensoren op het **witte** vlak en stuur `calibrate white`.
2. Zet de robot met alle sensoren op de **zwarte** lijn en stuur `calibrate black`.
3. De waarden worden opgeslagen en blijven bewaard na uitschakelen. Herhaal dit bij ander licht of een andere ondergrond.

### settings
De robot rijdt stabiel met volgende parameters:  
(in te vullen na het afstellen op het parcours)

### start/stop button
- De start/stop-knop zit aan de **linkerrand**, ter hoogte van de ESP32.
- Eén druk = start, nog een druk = stop. De ingebouwde RGB-led toont de toestand: **groen = rijden, rood = stil**.
- De aan/uit-schakelaar **SW1** zit links achteraan, naast de batterijstekker. De power-led brandt als de robot aan staat.
