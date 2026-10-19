// lf_cmd.h - commando's om parameters te lezen en te zetten ("set kp 0.03", "get", "get kp").
// Portable: de firmware geeft een tekstregel binnen en krijgt het antwoord terug in een buffer.
#pragma once
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "lf_params.h"

namespace lf {

// Splitst een regel in woorden (in place). Geeft het aantal woorden.
inline int splits(char *regel, char *woord[], int max) {
  int n = 0;
  for (char *t = strtok(regel, " \t\r\n"); t && n < max; t = strtok(nullptr, " \t\r\n")) woord[n++] = t;
  return n;
}

// Behandelt "set <naam> <waarde>", "get" en "get <naam>". Geeft false als het een ander commando is.
inline bool param_commando(Params &p, int n, char *woord[], char *uit, int uitlen) {
  if (n >= 1 && strcmp(woord[0], "get") == 0) {
    int pos = 0;
    for (int i = 0; i < N_PARAMS && pos < uitlen - 64; i++) {
      if (n >= 2 && strcmp(woord[1], PARAM_DEFS[i].naam) != 0) continue;
      pos += snprintf(uit + pos, uitlen - pos, "%-9s %10.5g   %s\n", PARAM_DEFS[i].naam,
                      (double)(p.*(PARAM_DEFS[i].veld)), PARAM_DEFS[i].uitleg);
    }
    if (pos == 0) snprintf(uit, uitlen, "onbekende parameter: %s\n", woord[1]);
    return true;
  }
  if (n >= 1 && strcmp(woord[0], "set") == 0) {
    if (n < 3) { snprintf(uit, uitlen, "gebruik: set <naam> <waarde>\n"); return true; }
    float w = (float)atof(woord[2]);
    if (strcmp(woord[2], "on") == 0) w = 1;
    if (strcmp(woord[2], "off") == 0) w = 0;
    if (zet_param(p, woord[1], w))
      snprintf(uit, uitlen, "%s = %g\n", woord[1], (double)(p.*(zoek_param(woord[1])->veld)));
    else
      snprintf(uit, uitlen, "onbekende parameter: %s (typ 'get' voor de lijst)\n", woord[1]);
    return true;
  }
  return false;
}

}  // namespace lf
