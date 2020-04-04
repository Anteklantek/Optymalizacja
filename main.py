from typing import List
import itertools

import pandas as pd


def odleglosc(miasto_a: str, miasto_b: str):
    a = odleglosci.loc[odleglosci['city'] == miasto_a]
    return a[miasto_b]._values[0]

def oblicz_dlugosc_trasy(trasa: List[str]):
    suma_odleglosci: float = 0
    for i, miasto in enumerate(trasa):
        if(i == len(trasa)-1):
            break
        nastepne_miasto = trasa[i+1]
        suma_odleglosci += odleglosc(miasto, nastepne_miasto)
    return suma_odleglosci


def oblicz_najkrotsza_trase(trasa: List[str]):
    kolejnosci: List[List[str]] = list(itertools.permutations(trasa, len(trasa)))
    najkrotsza_trasa: float = 100000000000000000
    for kolejnosc in kolejnosci:
        dlugosc_trasy = oblicz_dlugosc_trasy(kolejnosc)
        if dlugosc_trasy < najkrotsza_trasa:
            najkrotsza_trasa = dlugosc_trasy
    return najkrotsza_trasa

wagi = pd.read_csv('./wagi_miast.csv')
wagi.sort_values("srednia_waga", axis = 0, ascending = False,
                 inplace = True, na_position ='last')
najwieksze_5 = wagi[0:5]
odleglosci = pd.read_csv('./odleglosci.csv')
trasa = najwieksze_5["Nazwa"].tolist()

limit = 100

def znajdz_najlepsza_trase_z_limitem(limit: int, dotychczasowa_trasa: List[str], liczba_miast: int):
    miasta = wagi["Nazwa"].tolist()[:]
    miasta = [miasto for miasto in miasta if miasto not in dotychczasowa_trasa]
    if len(dotychczasowa_trasa) == liczba_miast:
        print(f"Liczę kombinację: {dotychczasowa_trasa}")
        dlugosc_najkrotszej_trasy = oblicz_najkrotsza_trase(dotychczasowa_trasa)
        return dlugosc_najkrotszej_trasy, dotychczasowa_trasa[:]
    for miasto in miasta:
        dotychczasowa_trasa.append(miasto)
        kopia = dotychczasowa_trasa[:]
        dlugosc_trasy, trasa = znajdz_najlepsza_trase_z_limitem(limit, kopia, liczba_miast)
        if dlugosc_trasy < limit:
            return dlugosc_trasy, trasa
        else:
            dotychczasowa_trasa = dotychczasowa_trasa[:-1]
    return limit + 1, []


def znajdz_najlepsza_trase_z_limitem_wg_kolumn(limit: int, dotychczasowa_trasa: List[str], liczba_miast: int, kolumny: List[str]):
    # wagi = wyliczane na podstawie wczytanego pliku z parametru kolumny z funkcji
    return znajdz_najlepsza_trase_z_limitem(limit, dotychczasowa_trasa, liczba_miast)


print(znajdz_najlepsza_trase_z_limitem(30, [], 3))

"""
#Pomysły
- liczenie długości tras bez permutacji "lustrzanych" CAB == BAC -> tylko od tyłu, da tę samą długość
- doimplementowanie metody "znajdz_najlepsza_trase_z_limitem_wg_kolumn"
- pokazanie trasy na mapie
"""
















