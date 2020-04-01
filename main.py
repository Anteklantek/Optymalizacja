from typing import List
import itertools

import pandas as pd

def odleglosc(miasto_a: str, miasto_b: str):
    print(f"liczę odległość między {miasto_a} a {miasto_b}")
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

print(oblicz_najkrotsza_trase(trasa))
