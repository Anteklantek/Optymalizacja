from typing import List
import itertools

import pandas as pd
import numpy as np
from pandas import DataFrame


def odleglosc(miasto_a: str, miasto_b: str):                                                                            # funkcja liczaca odleglosc pomiedzy dwoma miastami
    a = odleglosci.loc[odleglosci['city'] == miasto_a]                                                                  # odwolanie sie do tabeli odleglosci, w ktorej to sa odleglosci pomiedzy poszzczegolnymi miastami
    return a[miasto_b]._values[0]                                                                                       # zwroc odleglosc pomiedzy podanymi miastami

def oblicz_dlugosc_trasy(trasa: List[str]):                                                                             # liczymy dlugosc trasy, danej lista
    suma_odleglosci: float = 0                                                                                          # zerujemy licznik sumy odleglosci, ktora bedzie wzrastac po kazdym dodaniu odleglosci
    for i, miasto in enumerate(trasa):                                                                                  # petla dzieki ktorej bedzie mozliwe liczenie dlugosci i dodawanie kolejnych odleglosci
        if(i == len(trasa)-1):
            break
        nastepne_miasto = trasa[i+1]
        suma_odleglosci += odleglosc(miasto, nastepne_miasto)
    return suma_odleglosci                                                                                              # zwrocona zostaje suma odleglosci


def oblicz_najkrotsza_trase(trasa: List[str]):                                                                          # funkcja liczaca najkrotsza trase
    kolejnosci: List[List[str]] = list(itertools.permutations(trasa, len(trasa)))                                       # odwolanie sie funkcji do samej siebie (rekurencja)
    najkrotsza_trasa: float = 10000                                                                                     # ustalenie poczatkowe jaka jest najkrotsza trasa, oczywiscie moze byc nadpisywana
    for kolejnosc in kolejnosci:                                                                                        # petla przeliczajaca nam najkrotsza trase (kolejnosci to kolejne miasta)
        dlugosc_trasy = oblicz_dlugosc_trasy(kolejnosc)                                                                 # obliczanie dlugosci trasy na podstawie wyzszej funkcji
        if dlugosc_trasy < najkrotsza_trasa:                                                                            # jezeli obecnie obliczona odleglosci miedzy miastami jest krotsza niz najkrotsza trasa
            najkrotsza_trasa = dlugosc_trasy                                                                            # nadpisz najkrotsza trase
    return najkrotsza_trasa                                                                                             # zwraca nam najkrotsza obliczona trase

'''
def wybrana_kolumna(wedlug: str)
        wagi = pd.read_csv('./wagi_miast.csv')                                                                          # wczytanie tabeli z miastami
        wagi.sort_values(wedlug, axis = 0, ascending = False,                                                           # posortowanie danych w tabeli wedlug wagi od najwyzszej do najnizszej
                 inplace = True, na_position ='last')
        return wagi.sort_values

najwieksze_5 = wagi[0:5]                                                                                                # funkcja dla 5 najwyzzych miast z najwyzszymi wagami
odleglosci = pd.read_csv('./odleglosci.csv')                                                                            # wczytanie tabeli z odleglosciami miedzy miastami
trasa = najwieksze_5["Nazwa"].tolist()                                                                                  # wziecie pod uwage trasy z 5 najwiekszymi wartosciami biorac pod uwage miasta (kolumna miasta)
'''

def znajdz_najlepsza_trase_z_limitem(limit: int, dotychczasowa_trasa: List[str], liczba_miast: int, wagi: DataFrame):   # funkcja wlasciwa ktora oblicza nam trase miedzy zadanymi miastami biorac pod uwage specjalne parametry
    miasta = wagi["Nazwa"].tolist()[:]                                                                                  # pusta lista miasta bioraca pod uwage kolumne z miastami
    miasta = [miasto for miasto in miasta if miasto not in dotychczasowa_trasa]                                         # umozliwia nam dodanie do tabeli miasta z uwzglednieniem zeby sie ono nie powtorzylo stad "not in"
    if len(dotychczasowa_trasa) == liczba_miast:                                                                        # jezeli dlugosc tabelki z dotychczasowymi miastami jest rowna liczbie miast
        print(f"Liczę kombinację: {dotychczasowa_trasa}")                                                               # oblicza kombinacje dla danej trasy (pomiedzy jednym miastem a drugim)
        dlugosc_najkrotszej_trasy = oblicz_najkrotsza_trase(dotychczasowa_trasa)                                        # uzywamy funkcji dlugosc najkrotszej trasy
        return dlugosc_najkrotszej_trasy, dotychczasowa_trasa[:]                                                        # zwraca nam
    for miasto in miasta:                                                                                               # kolejna petla
        dotychczasowa_trasa.append(miasto)                                                                              # dodaje nam miasto do dotychczasowej trasy
        kopia = dotychczasowa_trasa[:]                                                                                  # kopia, ktora umozliwi rekurencje (odwolanie sie do samej siebie)
        dlugosc_trasy, trasa = znajdz_najlepsza_trase_z_limitem(limit, kopia, liczba_miast,wagi)                             # znajduje nam trase z najlepsza dlugoscia dla danych miast (optymalne rozwiazanie)
        if dlugosc_trasy < limit:                                                                                       # jezeli dlugosc trasy NIE przekrasza podanego w parametrach kryterium (np. 1500km)
            return dlugosc_trasy, trasa                                                                                 # zwroc dlugosc trasy
        #if len(kopia) >= 5 and limit <=750 and dlugosc_trasy < limit:                                                  # zabezpieczenie gdy dlugosc trasy jest bardzo mala a miast jest duzo zeby eliminowal wiecej krokow
        #   dotychczasowa_trasa = dotychczasowa_trasa[:-5]                                                              # ale srednio dziala bo potem i tak przywraca te same trasy na zmiane :(
        else:                                                                                                           # jezeli przekracza ta dlugosc
            dotychczasowa_trasa = dotychczasowa_trasa[:-1]                                                              # usun poprzednie miasto z funkcji i policz inaczej (przez inne miasto)
    return limit + 1, []                                                                                                # zwroc wynik najlepszej trasy


def znajdz_najlepsza_trase_z_limitem_wg_kolumn(limit: int, dotychczasowa_trasa: List[str], liczba_miast: int, kolumna: str):
    wagi = pd.read_csv('./wagi_miast.csv')
    wagi.sort_values(kolumna, axis=0, ascending=False,                                                                  # posortowanie danych w tabeli wedlug wagi od najwyzszej do najnizszej
                     inplace=True, na_position='last')
    return znajdz_najlepsza_trase_z_limitem(limit, dotychczasowa_trasa, liczba_miast, wagi)

wagi = pd.read_csv('./wagi_miast.csv')                                                                                  # wczytanie tabeli z miastami
wagi.sort_values("srednia_waga", axis = 0, ascending = False,                                                           # posortowanie danych w tabeli wedlug wagi od najwyzszej do najnizszej
                 inplace = True, na_position ='last')
najwieksze_5 = wagi[0:5]                                                                                                # funkcja dla 5 najwyzzych miast z najwyzszymi wagami
odleglosci = pd.read_csv('./odleglosci.csv')                                                                            # wczytanie tabeli z odleglosciami miedzy miastami
trasa = najwieksze_5["Nazwa"].tolist()

#def wygeneruj_najlepsza_trase_na_mapie():

# Zadanie 1
print("Zadanie 1:")
print(znajdz_najlepsza_trase_z_limitem(1500, [], 5,wagi))

# Zadanie 2
# wprowdzilem element losowosci, zeby pasowalo to do dowolnej ilosc miast lub dowolnej odleglosci zsumowanej miedzy miastami
odl_los = np.random.randint(3000)
probki = np.random.randint(10)

# tutaj pokazuje jaka jest zadana przez dwie powyzsze zmienne: ilosc miast i odleglosc
print(odl_los)
print(probki)

print("Zadanie 2:")
print(znajdz_najlepsza_trase_z_limitem(odl_los, [], probki,wagi))


# Zadanie 3
max_odl = int(input("Podaj maksymalną odległość: "))
ilosc_miast = int(input("Podaj ilosć miast: "))
kolumna = str(input("Podaj kolumne: "))

print("Zadanie 3:")
print(znajdz_najlepsza_trase_z_limitem_wg_kolumn(max_odl,[],ilosc_miast,kolumna))

# Zadanie 4


"""
#Pomysły
- liczenie długości tras bez permutacji "lustrzanych" CAB == BAC -> tylko od tyłu, da tę samą długość
- doimplementowanie metody "znajdz_najlepsza_trase_z_limitem_wg_kolumn"
- pokazanie trasy na mapie
"""
