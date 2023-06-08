import sys
import os
import urllib.request
import requests
import csv

def download_names(group_name):
    given_names_root = 'http://archive.nytud.hu/oszt/nyelvmuvelo/utonevek'
    
    print(f'checking {group_name}')
    group_filename = f'{group_name}.txt'
    if not os.path.isfile(group_filename):
        print(f'{group_filename} file missing. Downloading it from www.nytud.mta.hu')
        names_url = f'{given_names_root}/{group_name}.txt'
        with urllib.request.urlopen(names_url) as response:
            content = response.read().decode('ISO-8859-2')
            converted_content = content.encode('UTF-8')
            converted_content = converted_content.decode('UTF-8')
            with open(group_filename, 'w') as file:
                file.write(converted_content)
        print(f'{group_filename} is ready.')
        return True
    else:
        print(f'{group_filename} exists. Passing.')

def load_names(filename):
    if not os.path.isfile(filename):
        print(f'{filename} does not exists.')
        sys.exit(1)

    with open(filename, 'r') as file:
        names = [sor.strip().lower() for sor in file.readlines()]
        names = names[1:]
    return names

def download_resource(name):
    url = f'http://agrartamapi.code4.hu/api/{name}'

    print(f'Downloading resource <{name}>')

    response = requests.get(url);

    if response.status_code == 200:
        json_data = response.json()
        print('Downloaded.')
        return json_data['data']
    else:
        print(f'Error while downloading resource <{name}>: {response.status_code}')
        sys.exit(1)

def json_keres(mit, hol, holkulcs):
    for el in hol:
        if el[holkulcs] == mit:
            return el
        
def write_marked_rows_to_file(csv_file, updated_rows):
    print(f'Writing to {csv_file}')
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(updated_rows[0])
        
        for row in updated_rows[1:]:
            writer.writerow(row)
    print(f'{csv_file} written.')