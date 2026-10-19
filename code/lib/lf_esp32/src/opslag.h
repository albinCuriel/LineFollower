// opslag.h - parameters en kalibratie bewaren in het flashgeheugen (NVS = de "EEPROM" van de ESP32).
#pragma once
#include <Preferences.h>
#include "lf_core.h"

namespace opslag {

static const uint32_t VERSIE = 2;   // verhogen als struct Params verandert -> oude data wordt genegeerd

inline bool laad(lf::Params &p, lf::Kalibratie &k) {
  Preferences pref;
  pref.begin("lf", true);
  bool ok = pref.getUInt("versie", 0) == VERSIE &&
            pref.getBytesLength("params") == sizeof(lf::Params) &&
            pref.getBytesLength("kal") == sizeof(lf::Kalibratie);
  if (ok) {
    pref.getBytes("params", &p, sizeof(p));
    pref.getBytes("kal", &k, sizeof(k));
  }
  pref.end();
  return ok;
}

inline void bewaar(const lf::Params &p, const lf::Kalibratie &k) {
  Preferences pref;
  pref.begin("lf", false);
  pref.putUInt("versie", VERSIE);
  pref.putBytes("params", &p, sizeof(p));
  pref.putBytes("kal", &k, sizeof(k));
  pref.end();
}

}  // namespace opslag
