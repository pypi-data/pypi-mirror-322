import bukmacherska as bk

# Przykładowe użycie funkcji obliczeniowych
srednia1_zdobytych, liczba_goli1 = bk.oblicz_wynik_druzyny(10, 5, 3)
print(f"Drużyna 1 - Średnia zdobytych goli: {srednia1_zdobytych}, Liczba zdobytych goli: {liczba_goli1}")

# Importuj wszystkie funkcje z pliku bukmacherska.py
from .bukmacherska import (
    gamma_function,
    beta_function,
    poisson_probability,
    poisson_integral,
    calculate_C,
    poisson_cdf,
    expected_value,
    median,
    variance,
    entropy,
    eta_squared,
    oblicz_wynik_druzyny,
    oblicz_wynik_druzyny2,
    okresl_typ_meczu,
    f_x_a_b,
    f_x_a_minus_b,
    calculate_beta_integral,
    calculate_a_integral,
    rysuj_wykresy,
    tabela_wartosci_gamma,
    drukuj_tabele_gamma
)

