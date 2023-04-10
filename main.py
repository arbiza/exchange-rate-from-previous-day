import pandas
import argparse

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description='Returns the exchange rate from the previous business day',
        epilog='Project https://github.com/arbiza/exchange-rate-from-previous-day')

    parser.add_argument('-f', dest='cvs_file', type=str, nargs=1, required=True,
                        help='Path to the CVS file with the exchange rates')
    parser.add_argument('-c', dest='currency', type=str, nargs=1, required=True,
                        help='Currency symbol as it appears in the CVS file (e.g.: USD,AUD,HKD,NZD,EUR,GBP)')
    parser.add_argument('-d', dest='dates', type=str, nargs='+', required=True,
                        help='List of transaction dates (e.g.: 2023-02-14 2023-03-30)')

    args = parser.parse_args()

    cvs_content = pandas.read_csv(
        args.cvs_file[0], sep=';', encoding='ISO-8859-1')
    print(cvs_content)
