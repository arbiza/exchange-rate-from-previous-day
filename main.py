# Copyright 2023 Lucas Arbiza <lucas.arbiza@gmail.com>
#
# Returns the list of exchange rates of a given currency on the day before the
# transaction date(s)
#
# USAGE:
#   Run "python main.py -h" for up to date options

import pandas
import argparse
from datetime import datetime
from dateutil import parser, tz


if __name__ == "__main__":

    arg_parser = argparse.ArgumentParser(
        description='Returns the exchange rate from the previous business day',
        epilog='Project https://github.com/arbiza/exchange-rate-from-previous-day',
        formatter_class=argparse.RawTextHelpFormatter)

    arg_parser.add_argument('-f', dest='cvs_file', type=str, nargs=1, required=True,
                            help='Path to the CVS file with the exchange rates')
    arg_parser.add_argument('-c', dest='currency', type=str, nargs=1, required=True,
                            help='Currency symbol as it appears in the CVS file (e.g.: USD,AUD,HKD,NZD,EUR,GBP)')
    arg_parser.add_argument('-d', dest='transaction_dates', type=str, nargs='+', required=True,
                            help='List of transaction dates\n'
                                 'Accepted formats:\n'
                                 ' - 2023-04-12T04:37:09+0200\n'
                                 ' - 2023-04-12T04:39:01.700316129+0200\n'
                                 ' - 20230412\n'
                                 ' - 2023-04-12'
                            )
    arg_parser.add_argument('-i', dest='index', type=str, nargs=1, required=True,
                            help='Name of the \'date\' column')
    arg_parser.add_argument('--sep', type=str, nargs=1, required=False,
                            help='CSV separator (default is \',\')')
    arg_parser.add_argument('--tz', dest='in_tz', type=str, nargs=1, required=False,
                            help='Timezone of the provided dates as in /usr/share/zoneinfo/')
    arg_parser.add_argument('--cvs-tz', dest='cvs_tz', type=str, nargs=1, required=False,
                            help='Timezone of the data in the CVS file as in /usr/share/zoneinfo/ (if not informed, it will use the local TZ)')
    arg_parser.add_argument('--detail', type=bool, action=argparse.BooleanOptionalAction,
                            help='for an detailed output')

    args = arg_parser.parse_args()
    date = args.index[0]
    currency = args.currency[0]

    df = pandas.read_csv(
        args.cvs_file[0], sep=',' if args.sep is None else args.sep[0], encoding='ISO-8859-1')

    tz_cvs = tz.tzlocal() if args.cvs_tz is None else tz.gettz(args.cvs_tz[0])
    tz_input = tz.tzlocal() if args.in_tz is None else tz.gettz(args.in_tz[0])

    # Reduces the dataframe and stay with the minimun
    df = df[[date, currency]]

    not_a_date = list()

    for index, row in df.iterrows():
        try:
            d = parser.parse(row[date]).replace(tzinfo=tz_cvs)
            row[date] = d.date()
        except:
            not_a_date.append(index)
            pass

    # Remove any row which doesn't start with a date and reset the index
    df = df.drop(not_a_date, axis=0)
    df = df.sort_values(date)
    df = df.reset_index(drop=True)

    transactions = [
        d2.astimezone(tz_cvs) for d2 in [
            parser.parse(d).replace(tzinfo=tz_input) for d in args.transaction_dates]]
    transactions = [d.date() for d in transactions]

    transactions.sort()

    j = 0
    found = list()
    for td in transactions:

        while j < len(df[date]):

            if td > df[date][j]:
                j += 1

            elif td < df[date][j]:
                break

            else:
                found.append(td)
                if args.detail:
                    print(
                        "Transaction date {} - Previous day {}      {}: {}".format(
                            td,
                            df[date][0 if j == 0 else j-1],
                            currency,
                            df[currency][0 if j == 0 else j-1]))
                else:
                    print(format(df[currency][0 if j == 0 else j-1]))
                break

    [transactions.remove(f) for f in found]

    print('\n' + '-' * 40 + '\n')
    print("Transaction out of range of {}:\n".format(args.cvs_file[0]))
    [print(" - {}".format(d)) for d in transactions]
