import csv
import sys

"""Run the program"""


def main():
    try:
        access_url_from_csv()
    except FileNotFoundError:
        print("File is not found.")


def access_url_from_csv():
    filename = sys.argv[1]
    # open stream
    with open(filename) as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=",")
        max_row = 5
        for row in csv_reader:
            url = row["Case Type"]
            max_row -= 1
            if max_row == 0:
                return


def start_scraper(url):
    # do scraper stuff here
    pass


if __name__ == "__main__":
    main()

