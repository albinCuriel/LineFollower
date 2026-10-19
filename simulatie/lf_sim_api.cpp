// lf_sim_api.cpp - C-interface rond de firmwarekern (code/lib/lf_core) zodat Python ze kan aanroepen.
// Bouwen (gebeurt automatisch door sim.py):
//   python -m ziglang c++ -shared -O2 -o lf_sim.dll lf_sim_api.cpp -I ../code/lib/lf_core/src
#include "lf_core.h"

#ifdef _WIN32
#define API extern "C" __declspec(dllexport)
#else
#define API extern "C"
#endif

API void *lf_nieuw() { return new lf::Regelaar(); }
API void lf_weg(void *r) { delete static_cast<lf::Regelaar *>(r); }

API int lf_zet(void *r, const char *naam, float waarde) {
  return lf::zet_param(static_cast<lf::Regelaar *>(r)->p, naam, waarde) ? 1 : 0;
}

API float lf_lees(void *r, const char *naam) {
  const lf::ParamDef *d = lf::zoek_param(naam);
  return d ? static_cast<lf::Regelaar *>(r)->p.*(d->veld) : -1e9f;
}

API void lf_kalibreer(void *r, const float *wit, const float *zwart) {
  auto *g = static_cast<lf::Regelaar *>(r);
  g->sensor.kal_wit(wit);
  g->sensor.kal_zwart(zwart);
}

API void lf_start(void *r, int aan) {
  auto *g = static_cast<lf::Regelaar *>(r);
  g->reset();
  g->rijden = aan != 0;
}

// uit[0..5] = duty_links, duty_rechts, positie_mm, v_doel, dv, lijn
API void lf_stap(void *r, const float *refl, float dt, float vbat, float vl, float vr, float *uit) {
  lf::Ingang in;
  for (int i = 0; i < lf::N_SENSOR; i++) in.refl[i] = refl[i];
  in.dt = dt; in.vbat = vbat; in.v_links = vl; in.v_rechts = vr;
  lf::Uitgang u = static_cast<lf::Regelaar *>(r)->stap(in);
  uit[0] = u.duty_links; uit[1] = u.duty_rechts; uit[2] = u.positie_mm;
  uit[3] = u.v_doel; uit[4] = u.dv; uit[5] = u.lijn ? 1.f : 0.f;
}
