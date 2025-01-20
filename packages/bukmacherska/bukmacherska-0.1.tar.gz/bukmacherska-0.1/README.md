# Bukmacherska

Biblioteka do obliczeń bukmacherskich.

## Instalacja

```bash
pip install bukmacherska

import bukmacherska as bk

# Przykładowe użycie funkcji obliczeniowych
srednia1_zdobytych, liczba_goli1 = bk.oblicz_wynik_druzyny(10, 5, 3)
print(f"Drużyna 1 - Średnia zdobytych goli: {srednia1_zdobytych}, Liczba zdobytych goli: {liczba_goli1}")

srednia2_zdobytych, liczba_goli2 = bk.oblicz_wynik_druzyny2(8, 6, 3)
print(f"Drużyna 2 - Średnia zdobytych goli: {srednia2_zdobytych}, Liczba zdobytych goli: {liczba_goli2}")

typ_meczu = bk.okresl_typ_meczu(srednia1_zdobytych, srednia2_zdobytych)
print(f"Typ meczu: {typ_meczu}")

# Przykładowe użycie funkcji rysujących wykresy
bk.rysuj_wykresy(srednia1_zdobytych, liczba_goli1, srednia2_zdobytych, liczba_goli2)



