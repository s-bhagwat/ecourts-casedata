import csv


def get_case_type_urls_from_csv():
    filename = 'data.csv'
    l = []
    line_count = 0

    # open stream
    with open(filename) as csv_file:
        # create a dict
        csv_reader = csv.DictReader(csv_file, delimiter=",")

        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            elif line_count < 3:
                line_count += 1
                continue
            else:
                d = {
                    'url': row["Case Type"],
                    'state_interim': row["StateFinal"],
                    'district_interim': row["DistrictFinal"]
                }
                l.append(d)
                line_count += 1

    return l

