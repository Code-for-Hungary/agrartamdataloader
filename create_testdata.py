with open('utf8_export.csv', 'r') as file:
    lines = [next(file) for _ in range(200)]

with open('testdata.csv', 'w') as output_file:
    for line in lines:
        output_file.write(line)
