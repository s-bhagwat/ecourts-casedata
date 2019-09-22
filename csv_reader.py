import csv


def get_urls():
    with open('data.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        l = []
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            elif line_count < 4:
                line_count += 1
                continue
            else:
                d = {
                    'url': row[17],
                    'state_interim': row[24],
                    'district_interim': row[26]
                }
                l.append(d)
                line_count += 1

    return l
