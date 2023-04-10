import pandas
import argparse
import re
from datetime import datetime


def datetime_handler(dt: str, dt_dict: dict, tz: str = None, cvs_tz: str = None):

    if dt_dict["yyyymmdd"].match(dt):
        print("{} matches 'yyyymmdd'".format(dt))
    elif dt_dict["dd_mm_yyyy"].match(dt):
        print("{} matches 'dd_mm_yyyy'".format(dt))
    elif dt_dict["yyyy_mm_dd_hh_mm_ss"].match(dt):
        print("{} matches 'yyyy_mm_dd_hh_mm_ss'".format(dt))
    elif dt_dict["iso_8601_date"].match(dt):
        print("{} matches 'iso_8601_date'".format(dt))
    elif dt_dict["iso_8601"].match(dt):
        print("{} matches 'iso_8601'".format(dt))


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description='Returns the exchange rate from the previous business day',
        epilog='Project https://github.com/arbiza/exchange-rate-from-previous-day')

    parser.add_argument('-f', dest='cvs_file', type=str, nargs=1, required=True,
                        help='Path to the CVS file with the exchange rates')
    parser.add_argument('-c', dest='currency', type=str, nargs=1, required=True,
                        help='Currency symbol as it appears in the CVS file (e.g.: USD,AUD,HKD,NZD,EUR,GBP)')
    parser.add_argument('-d', dest='transaction_dates', type=str, nargs='+', required=True,
                        help='List of transaction dates (e.g.: 2023-02-14 2023-03-30)')
    parser.add_argument('-i', dest='index', type=str, nargs=1, required=True,
                        help='Name of the \'date\' column')
    parser.add_argument('--in-tz', dest='in_timezone', type=str, nargs=1, required=False,
                        help='Timezone of the informed data')
    parser.add_argument('--cvs-tz', dest='local_timezone', type=str, nargs=1, required=False,
                        help='Timezone of the data in the CVS file')

    args = parser.parse_args()

    cvs_content = pandas.read_csv(
        args.cvs_file[0], sep=';', encoding='ISO-8859-1', parse_dates=['data'])
    # args.cvs_file[0], index_col=args.index[0], sep=';', encoding='ISO-8859-1', parse_dates=['data'])

    dt_dict = {
        "yyyymmdd": re.compile("^\d{8}$"),
        "dd_mm_yyyy": re.compile("^\d{2}-\d{2}-\d{4}$"),
        "yyyy_mm_dd_hh_mm_ss": re.compile("^\d{4} -\d{2} -\d{2} \d{2}: \d{2}: \d{2}$"),
        "iso_8601_date": re.compile("^\d{4}-\d{2}-\d{2}$"),
        "iso_8601": re.compile("^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?([+-]\d{2}:?\d{2}|[Zz])$")
    }

    datetime_handler("2023-04-10", dt_dict)
    datetime_handler("20230410", dt_dict)
    datetime_handler("2022-01-03", dt_dict)
    datetime_handler("03-01-2021", dt_dict)
    datetime_handler("2022-01-04T05:10:42.960148Z", dt_dict)
    datetime_handler("1994-11-05T08:15:30-05:00", dt_dict)
    datetime_handler("1994-11-05T08:15:30.989412-05:00", dt_dict)
    datetime_handler("1994-11-05T08:15:30.989412+05:00", dt_dict)
