# Simulatie: getunede parameters

Beste score: **7.42 s** (gemiddelde over 3 runs met sensorruis en -6/0/+6 % motorverschil).
Met 90 % van die snelheden (startwaarden voor de echte robot): **7.94 s**, gemiddeld 0.82 m/s.

Op de robot zetten (wifi-terminal of seriële monitor):
```
set kp 0.02669
set ki 0.02144
set kd 0.001451
set vbocht 0.7427
set vrecht 2.118
set erecht 7.659
set ebocht 23.6
set drem 171.3
set aboost 7.329
save
```

![resultaat](resultaat_tune.png)