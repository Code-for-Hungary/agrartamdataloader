import sys
import csv

def write_insert(file, records):
    file.write('INSERT INTO tamogatas VALUES \n')
    file.write(',\n'.join(records))
    file.write(';\n')

if len(sys.argv) < 3:
    print('Missing parameter.')
    print('Usage')
    print(f'    {sys.argv[0]} source_file target_file record_per_file record_per_insert')
    print('     target_file - without extension')
    print('     record_per_file - default = 50000')
    print('     record_per_insert - default = 1000')
    print('')
    sys.exit(1)

source_filename = sys.argv[1]
target_filename = sys.argv[2]
recordperfile = int(sys.argv[3])
if not recordperfile:
    recordperfile = 50000
recordperinsert = int(sys.argv[4])
if not recordperinsert:
    recordperinsert = 1000

records = []

file_count = 0
output_files = []
output_file = open(f"{target_filename}_{file_count+1}.sql", "w")
output_files.append(output_file)

with open(source_filename, 'r') as source_file:
    reader = csv.reader(source_file, delimiter=';')
    for row_number, row in enumerate(reader, start=1):
        if row_number == 1:
            continue

        records.append(f'("{row[0]}","{row[1]}")')

        if row_number % recordperinsert == 0:
            write_insert(output_file, records)
            records = []
            
        if row_number % recordperfile == 0:
            if records:
                write_insert(output_file, records)
                records = []

            output_file.close()
            file_count += 1
            output_file = open(f"{target_filename}_{file_count+1}.sql", "w")
            output_files.append(output_file)

if records:
    write_insert(output_file, records)
    records = []

# Fájlok bezárása
for output_file in output_files:
    output_file.close()

print(f"Létrehozott fájlok száma: {file_count+1}")
