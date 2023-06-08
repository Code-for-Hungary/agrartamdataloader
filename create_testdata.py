import sys

if len(sys.argv) < 4:
    print('Missing parameter.')
    print('Usage')
    print(f'    {sys.argv[0]} source_file target_file line_num')
    print('')
    sys.exit(1)

source_filename = sys.argv[1]
target_filename = sys.argv[2]
recno = int(sys.argv[3])

with open(source_filename, 'r') as file:
    lines = [next(file) for _ in range(recno)]

with open(target_filename, 'w') as output_file:
    for line in lines:
        output_file.write(line)

print('Ready. Bye.')
