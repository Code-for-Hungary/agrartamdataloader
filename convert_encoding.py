import sys
import os
import codecs

from_encoding = 'iso-8859-2'
to_encoding = 'utf-8'

if len(sys.argv) < 2:
    print('Nincs megadva fájlnév.')
    sys.exit(1)

csv_file = sys.argv[1]
target_filename = f'utf8_{csv_file}'
if not os.path.exists(target_filename):
    print(f'Converting {csv_file}')
    with codecs.open(csv_file, 'r', from_encoding) as source_file:
        with codecs.open(target_filename, 'w', to_encoding) as target_file:
            for line in source_file:
                converted_line = line.encode(to_encoding).decode(to_encoding)
                target_file.write(converted_line)
    print('Ready.')
else:
    print(f'{target_filename} is already there, not re-encoding it.')
