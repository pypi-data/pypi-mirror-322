# test_bukmacherska.py
import bukmacherska as bk

# Przykładowe użycie funkcji obliczeniowych
srednia1_zdobytych, liczba_goli1 = bk.oblicz_wynik_druzyny(10, 5, 3)
print(f"Drużyna 1 - Średnia zdobytych goli: {srednia1_zdobytych}, Liczba zdobytych goli: {liczba_goli1}")

srednia2_zdobytych, liczba_goli2 = bk.oblicz_wynik_druzyny2(12, 6, 4)
print(f"Drużyna 2 - Średnia zdobytych goli: {srednia2_zdobytych}, Liczba zdobytych goli: {liczba_goli2}")

typ_meczu = bk.okresl_typ_meczu(srednia1_zdobytych, srednia2_zdobytych)
print(f"Typ meczu: {typ_meczu}")

# Testowanie innych funkcji
gamma_val = bk.gamma_function(5)
print(f"Gamma(5): {gamma_val}")

poisson_prob = bk.poisson_probability(3, 2)
print(f"Poisson Probability (3, 2): {poisson_prob}")

median_val = bk.median(4.5)
print(f"Median(4.5): {median_val}")

entropy_val = bk.entropy(2.5)
print(f"Entropy(2.5): {entropy_val}")

# Testowanie funkcji rysujących wykresy (opcjonalne)
# bk.rysuj_wykresy(srednia1_zdobytych, liczba_goli1, srednia2_zdobytych, liczba_goli2)
