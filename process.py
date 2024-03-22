import csv
import sys
import os
import datetime
import agrarhelpers

def mark_rows(csv_file):
    print('Processing')

    marked_rows = []

    hjogcim = []
    halap = []
    hforras = []

    with open(csv_file, 'r') as file:
        reader = csv.reader(file, delimiter=';')
        header = next(reader)
        header.append('Year')
        header.append('Firm')
        header.append('Gender')
        header.append('JogcimID')
        header.append('AlapID')
        header.append('ForrasID')
        header.append('Landbased')
        header.append('Telepules')
        header.append('Megye')
        marked_rows.append(header)
        
        for row in reader:
            row.append(year)

            nev = row[0].lower()
            if is_firm(nev):
                row.append('1')
                row.append('')
            else:
                row.append('0')
                keresztnev = nev.split()[-1];
                if keresztnev in female_names or keresztnev.endswith('né'):
                    row.append('female')
                else:
                    if keresztnev in male_names:
                        row.append('male')
                    else:
                        row.append('')

            # jogcim
            jogcim = agrarhelpers.json_keres(row[4], jogcimek, 'name')
            if jogcim:
                row.append(jogcim['id'])
            else:
                if row[4] not in hjogcim:
                    hjogcim.append(row[4])
                row.append('')

            # alap
            alap = agrarhelpers.json_keres(row[5], alapok, 'name')
            if alap:
                row.append(alap['id'])
            else:
                if row[5] not in halap:
                    halap.append(row[5])
                row.append('')

            # forras
            forras = agrarhelpers.json_keres(row[6], forrasok, 'name')
            if forras:
                row.append(forras['id'])
            else:
                if row[6] not in hforras:
                    hforras.append(row[6])
                row.append('')

            if row[4] in ['Területalapú támogatás', 'Zöldítés támogatás igénylése']:
                row.append('1')
            else:
                row.append('0')

            # telepules, megye
            telepules = agrarhelpers.json_keres(row[1], telepulesek, 'irszam')
            if telepules:
                row.append(telepules['id'])
                row.append(telepules['megye_id'])
            else:
                row.append('')
                row.append('')

            # cegcsoport
            # tamogatott

            marked_rows.append(row)
    
    of = open('kapcs.sql', 'w');
    for s in hjogcim:
        of.write(f"INSERT INTO jogcims (name, sorrend) VALUES (\"{s}\", 99888);\n")

    for s in halap:
        of.write(f"INSERT INTO alaps (name, sorrend) VALUES (\"{s}\", 99888);\n")

    for s in hforras:
        of.write(f"INSERT INTO jogcims (name) VALUES (\"{s}\");\n")

    of.close()

    return marked_rows

def is_firm(name):
    result = False
    for firm_name in firm_names:
        if firm_name in name:
            result = True
    return result

print(datetime.datetime.now())

if len(sys.argv) < 4:
    print('Missing parameter.')
    print('Usage')
    print(f'    {sys.argv[0]} source_file target_file year')
    print('')
    sys.exit(1)

source_filename = sys.argv[1]
target_filename = sys.argv[2]
year = sys.argv[3]

if not os.path.exists(target_filename):

    if agrarhelpers.download_names('osszesnoi') and os.path.isfile('women.txt'):
        with open('women.txt', 'r') as forras_file, open('osszesnoi.txt', 'a') as cel_file:
            for sor in forras_file:
                cel_file.write(sor)

    if agrarhelpers.download_names('osszesffi') and os.path.isfile('men.txt'):
        with open('men.txt', 'r') as forras_file, open('osszesffi.txt', 'a') as cel_file:
            for sor in forras_file:
                cel_file.write(sor)


    female_names = agrarhelpers.load_names('osszesnoi.txt')
    male_names = agrarhelpers.load_names('osszesffi.txt')

    jogcimek = agrarhelpers.download_resource('jogcims')
    alapok = agrarhelpers.download_resource('alaps')
    forrasok = agrarhelpers.download_resource('forras')
    cegcsoportok = agrarhelpers.download_resource('cegcsoports')
    tamogatottak = agrarhelpers.download_resource('tamogatotts')
    megyek = agrarhelpers.download_resource('megyes')
    telepulesek = agrarhelpers.download_resource('telepules')

    with open('firm_keywords.txt', 'r') as file:
        firm_names = [sor.strip().lower() for sor in file.readlines()]

    marked_rows = mark_rows(source_filename)
    agrarhelpers.write_marked_rows_to_file(target_filename, marked_rows)

    print('Ready. Bye.')
else:
    print(f'{target_filename} is already there, exiting.')

print(datetime.datetime.now())
