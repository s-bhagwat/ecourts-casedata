import csv
import sys

"""Run the program"""


def main():
    try:
        access_url_from_csv()
    except FileNotFoundError:
        print("File is not found.")


def access_url_from_csv():
    # set up default behaviour if no cli arg is given
    if len(sys.argv < 2):
        filename = "court_url.csv"
    else:
        filename = sys.argv[1]

    # open stream
    with open(filename) as csv_file:
        # create a dict
        csv_reader = csv.DictReader(csv_file, delimiter=",")

        # set a max row value
        max_row = 5
        for row in csv_reader:
            start_scraper(row["Case Type"])
            max_row -= 1
            if max_row == 0:
                # ends it early so we don't have to loop through 100s of page
                return


def start_scraper(url):
    # do scraper stuff here
    pass


if __name__ == "__main__":
    main()

