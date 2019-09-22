import csv
import json


def get_case_type_urls_from_csv():
    filename = 'data.csv'
    data = []
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
                    'state_name': row["State Display Name"],
                    'state_interim': row["StateFinal"],
                    'district_interim': row["DistrictFinal"]
                }
                data.append(d)
                line_count += 1

    return data


def write_dict_into_json_file(file_name, dict_):
    with open(file_name, "w+") as json_file:
        json.dump(dict_, json_file)
