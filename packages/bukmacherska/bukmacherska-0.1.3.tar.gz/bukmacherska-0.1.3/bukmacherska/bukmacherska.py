import math
import numpy as np
import scipy.integrate as integrate
from scipy.special import gamma, gammainc, factorial
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Stała Eulera
euler_const = 0.5772156649

# Funkcje gamma i beta
def gamma_function(x):
    if int(x) == x and x <= 0:
        raise ValueError("Gamma function not defined for non-positive integers.")
    return gamma(x)

def beta_function(x, a, b):
    numerator = gamma(a) * gamma(b)
    denominator = gamma(a + b)
    return numerator / denominator

# Funkcje pomocnicze
def poisson_probability(beta, alpha):
    return (math.exp(-alpha) * (alpha ** beta)) / factorial(beta)

def poisson_integral(x, lmbda, k):
    return (lmbda ** k * math.exp(-lmbda)) / factorial(k) * math.log(x)

def calculate_C(lmbda, k, gamma_value):
    poisson_prob = poisson_probability(k, lmbda)
    return poisson_prob * gamma_value**3 * lmbda

def poisson_cdf(gamma, alpha):
    return gammainc(gamma + 1, alpha) / factorial(gamma)

def expected_value(alpha):
    return alpha

def median(alpha):
    return math.floor(alpha + 1/3 - 0.02 / alpha)

def variance(alpha):
    return alpha

def entropy(alpha):
    term1 = 0.5 * math.log(2 * math.pi * alpha)
    term2 = -1 / (12 * alpha)
    term3 = -1 / (24 * alpha**2)
    term4 = -19 / (360 * alpha**3)
    return term1 + term2 + term3 + term4

def eta_squared(x):
    return x ** 2

# Funkcje obliczeniowe
def oblicz_srednia_zdobytych_goli(gole_zdobyte, bezposr_spotkania):
    return gole_zdobyte / bezposr_spotkania

def oblicz_srednia_straconych_goli(gole_stracone, bezposr_spotkania):
    return gole_stracone / bezposr_spotkania

def oblicz_wynik_druzyny(gole_zdobyte, gole_stracone, bezposr_spotkania):
    srednia_zdobytych = oblicz_srednia_zdobytych_goli(gole_zdobyte, bezposr_spotkania)
    srednia_straconych = oblicz_srednia_straconych_goli(gole_stracone, bezposr_spotkania)
    return srednia_zdobytych, srednia_straconych

def oblicz_wynik_druzyny2(gole_zdobyte, gole_stracone, bezposr_spotkania):
    srednia_zdobytych = oblicz_srednia_zdobytych_goli(gole_zdobyte, bezposr_spotkania)
    srednia_straconych = oblicz_srednia_straconych_goli(gole_stracone, bezposr_spotkania)
    return srednia_zdobytych, srednia_straconych

def okresl_typ_meczu(srednia1_zdobytych, srednia2_zdobytych):
    if srednia1_zdobytych > srednia2_zdobytych:
        return "Wygrany typ 1"
    elif srednia1_zdobytych < srednia2_zdobytych:
        return "Wygrany typ 2"
    else:
        return "Remis"

def f_x_a_b(B, delta, gamma_val):
    numerator = B + (delta + gamma_val)
    denominator = B + gamma_val
    return (numerator / denominator) ** 3

def f_x_a_minus_b(A, delta, gamma_val):
    numerator = A - (delta - gamma_val)
    denominator = A - gamma_val
    return (numerator / denominator) ** 3

def calculate_beta_integral(x, a, b):
    integrand = lambda t: t ** (a - 1) * (1 - t) ** (b - 1)
    integral, _ = integrate.quad(integrand, 0, x)
    return integral

def calculate_a_integral(x, a, b):
    integrand = lambda t: t ** (a + 1) * (1 + t) ** (b + 1)
    integral, _ = integrate.quad(integrand, 0, x)
    return integral

# Funkcje rysujące wykresy
def rysuj_wykresy(srednia1_zdobytych, srednia1_straconych, srednia2_zdobytych, srednia2_straconych):
    labels = ['Drużyna 1 Zdobyte', 'Drużyna 1 Stracone', 'Drużyna 2 Zdobyte', 'Drużyna 2 Stracone']
    values = [srednia1_zdobytych, srednia1_straconych, srednia2_zdobytych, srednia2_straconych]
    
    fig, axs = plt.subplots(2, 2, figsize=(12, 10))
    
    # Wykres Liniowy
    axs[0, 0].plot(labels, values, marker='o')
    axs[0, 0].set_title('Wykres Liniowy')
    axs[0, 0].set_ylabel('Liczba goli')
    axs[0, 0].set_xlabel('Kategorie')
    
    # Wykres Słupkowy
    axs[0, 1].bar(labels, values, color=['blue', 'red', 'green', 'orange'])
    axs[0, 1].set_title('Wykres Słupkowy')
    axs[0, 1].set_ylabel('Liczba goli')
    
    plt.show()

# Obliczenia dla tabeli wartości gamma
def tabela_wartosci_gamma(start, end):
    values = np.linspace(start, end, 30)
    table = [(x, gamma_function(x)) for x in values]
    return table

def drukuj_tabele_gamma(start, end):
    table = tabela_wartosci_gamma(start, end)
    print("Tabela Gamma(x):")
    for x, gamma_val in table:
        print(f"{x} | {gamma_val}")
