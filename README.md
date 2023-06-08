# K-Monitor Agrártámogatások adat előkészítő

Ez a program feldolgozza és az agrártámogatás keresőbe betölthető formára hozza a Magyar Államkincstár [honlapján](https://www.mvh.allamkincstar.gov.hu/tamogatasi-adatok) publikált támogatási "adatbázist".

## Használat

Töltsd le a fenti linkről a szükséges adat fájlt és csomagold ki  
Futtasd le az UTF-8-ra konvertálást.
``` 
python3 convert_encoding.py export.csv 
```
Ennek kimenete utf8_paraméter nevű fájl lesz, ebben az esetben utf8_export.csv.

Futtasd le a feldolgozó programot.
```
python3 process.py utf8_export.csv feldolgozott.csv 2022
```
Paraméterei sorban: forrás fájl, eredmény fájl, az adatok éve.

Az előzőleg létrejött fájlból a következő paranccsal csinálj SQL scriptet:
```
python3
```
Ezt az SQL scriptet töltsd be valahogy az adatbázisodba.

## Jó tudni

### osszesnoi.txt, osszesffi.txt

Az MTA weboldaláról letöltött fájlok amik a hivatalosan elfogadott női és férfi utónevek listáját tartalmazzák. Amelyikben a név utolsó szava szerepel teljes egyezéssel, olyan nemű a támogatott. "né" végződésűek (pl. Jánosné) szintén nőnek számítanak.
Ha ezek a fájlok nem léteznek, process.py letölti ezeket.

### women.txt, men.txt

Ezekben vannak a letöltött adatbázisban talált idegen nevek, elírások, a hivatalos utónév listából hiányzó nevek. Felhasználó által bővíthetők, a program nem írja felül csak használja ezeket. A két fájlt process.py hozzáadja a letöltött utónév listákhoz amikor letölti és konvertálja azokat. Ha létezik osszesffi.txt vagy osszesnoi.txt, akkor azzal egyáltalán nem foglalkozik.

### firm_keywords.txt

Ha az ebben szereplő kulcsszavak előfordulnak a csv 0. oszlopában, akkor a támogatott valószínűleg jogi személy.

### Terület alapú támogatás

Egyelőre be van égetve, hogy ha a jogcím (csv 5. oszlopa) 'Területalapú támogatás' vagy 'Zöldítés támogatás igénylése', akkor terület alapú támogatásról van szó.

### Jogcím, alap, forrás, megye, település

Ezeket az adatokat a program az agrártámogatás keresőtől kérdezi le a megfelelő API végpontokon keresztül. A csv-be az innen kikeresett ID-k kerülnek.

### Cégcsoport, támogatott

