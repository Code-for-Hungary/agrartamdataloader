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

Ha hiányoznak az agrár adatbázisból kapcsolódó adatok, akkor itt jön létre kapcs.sql. Ha a fájl nem üres, futtasd le az agrár adatbázison és utána futtasd újra ezt a lépést.

Töltsd be a feldolgozott.csv-t excelbe és nézd meg, hogy van-e sor üres településsel vagy üres megyével. Ha van, javítsd az agrár adatbázisban. Általában új "mellék" irányítószámon jelenik meg egy település vagy annak része, rögzítsd az adatbázisban (admin felület nincs, marad az SQL, bocs).

Az előzőleg létrejött fájlból a következő paranccsal csinálj SQL scriptet:
```
python3 tosql.py feldolgozott.csv betoltendo 50000 1000
```
A feldolgozott.csv-t feldarabolja és annyi betoltendo_N.sql fájlt generál belőle, amennyiben elfér 50000 sornyi adat 1000 soronként INSERTálva.  
Ha túl nagyok az sql fájlok, akkor először az első számot csökkentsd.  
Ha az adatbázis szerver még így sem bír betölteni egy fájlt, akkor csökkentsd a másodikat is.  
*Első szám >= második szám.*  
Az eredményül kapott SQL scripteket töltsd be valahogy az adatbázisodba.  
Ready. Bye.
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

### Tesztadatok

Ha egy évnél kevesebb adaton akarsz tesztelni valamit, használd a következő parancsot:
```
python3 create_testdata.py utf8_export.csv testdata.csv 200
```
Ezzel utf8_export.csv első 200 sorát kiírod testdata.csv-be.  
Ezután így futtasd process.py-t:
```
python3 process.py testdata.csv testeredmeny.csv 2022
```
