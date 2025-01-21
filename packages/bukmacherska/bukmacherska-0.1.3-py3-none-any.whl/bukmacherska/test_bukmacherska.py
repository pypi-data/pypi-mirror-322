import bukmacherska as bk

# Obliczanie średnich zdobytych i straconych goli
srednia1_zdobytych, srednia1_straconych = bk.oblicz_wynik_druzyny(10, 5, 3)
srednia2_zdobytych, srednia2_straconych = bk.oblicz_wynik_druzyny2(12, 6, 4)

# Wyświetlanie wyników
print(f"Drużyna 1 - Średnia zdobytych goli: {srednia1_zdobytych}, Średnia straconych goli: {srednia1_straconych}")
print(f"Drużyna 2 - Średnia zdobytych goli: {srednia2_zdobytych}, Średnia straconych goli: {srednia2_straconych}")

# Określenie typu meczu
typ_meczu = bk.okresl_typ_meczu(srednia1_zdobytych, srednia2_zdobytych)
print(f"Typ meczu: {typ_meczu}")

# Rysowanie wykresów
bk.rysuj_wykresy(srednia1_zdobytych, srednia1_straconych, srednia2_zdobytych, srednia2_straconych)
