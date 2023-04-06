import argparse

# Currency conversion rates
CONVERSION_RATES = {
    'AUDUSD': 0.8371,
    'CADUSD': 0.8711,
    'USDCNY': 6.1715,
    'EURUSD': 1.2315,
    'GBPUSD': 1.5683,
    'NZDUSD': 0.7750,
    'USDJPY': 119.95,
    'EURCZK': 27.6028,
    'EURDKK': 7.4405,
    'EURNOK': 8.6651,
}

# CROSS TABLE taken from PDF
CROSS_VIA_MATRIX = {
    'AUD': {'AUD': '1', 'CAD': 'USD', 'CNY': 'USD', 'CZK': 'USD', 'DKK': 'USD', 'EUR': 'USD', 'GBP': 'USD',
            'JPY': 'USD', 'NOK': 'USD', 'NZD': 'USD', 'USD': 'D'},
    'CAD': {'AUD': 'USD', 'CAD': '1', 'CNY': 'USD', 'CZK': 'USD', 'DKK': 'USD', 'EUR': 'USD', 'GBP': 'USD',
            'JPY': 'USD', 'NOK': 'USD', 'NZD': 'USD', 'USD': 'D'},
    'CNY': {'AUD': 'USD', 'CAD': 'USD', 'CNY': '1', 'CZK': 'USD', 'DKK': 'USD', 'EUR': 'USD', 'GBP': 'USD',
            'JPY': 'USD', 'NOK': 'USD', 'NZD': 'USD', 'USD': 'D'},
    'CZK': {'AUD': 'USD', 'CAD': 'USD', 'CNY': 'USD', 'CZK': '1', 'DKK': 'EUR', 'EUR': 'Inv', 'GBP': 'USD',
            'JPY': 'USD', 'NOK': 'EUR', 'NZD': 'USD', 'USD': 'EUR'},
    'DKK': {'AUD': 'USD', 'CAD': 'USD', 'CNY': 'USD', 'CZK': 'EUR', 'DKK': '1', 'EUR': 'Inv', 'GBP': 'USD',
            'JPY': 'USD', 'NOK': 'EUR', 'NZD': 'USD', 'USD': 'EUR'},
    'EUR': {'AUD': 'USD', 'CAD': 'USD', 'CNY': 'USD', 'CZK': 'D', 'DKK': 'D', 'EUR': '1', 'GBP': 'USD', 'JPY': 'USD',
            'NOK': 'USD', 'NZD': 'USD', 'USD': 'USD'},
    'GBP': {'AUD': 'USD', 'CAD': 'USD', 'CNY': 'USD', 'CZK': 'USD', 'DKK': 'USD', 'EUR': 'USD', 'GBP': '1',
            'JPY': 'USD', 'NOK': 'USD', 'NZD': 'USD', 'USD': 'D'},
    'JPY': {'AUD': 'USD', 'CAD': 'USD', 'CNY': 'USD', 'CZK': 'USD', 'DKK': 'USD', 'EUR': 'USD', 'GBP': 'USD',
            'JPY': '1', 'NOK': 'USD', 'NZD': 'USD', 'USD': 'Inv'},
    'NOK': {'AUD': 'USD', 'CAD': 'USD', 'CNY': 'USD', 'CZK': 'EUR', 'DKK': 'EUR', 'EUR': 'Inv', 'GBP': 'USD',
            'JPY': 'USD', 'NOK': '1', 'NZD': 'USD', 'USD': 'EUR'},
    'NZD': {'AUD': 'USD', 'CAD': 'USD', 'CNY': 'USD', 'CZK': 'USD', 'DKK': 'USD', 'EUR': 'USD', 'GBP': 'USD',
            'JPY': 'USD', 'NOK': 'USD', 'NZD': '1', 'USD': 'D'},
    'USD': {'AUD': 'Inv', 'CAD': 'Inv', 'CNY': 'Inv', 'CZK': 'EUR', 'DKK': 'EUR', 'EUR': 'Inv', 'GBP': 'Inv',
            'JPY': 'D', 'NOK': 'EUR', 'NZD': 'Inv', 'USD': '1'}
}


def convert_currency(amount=1, from_currency='USD', to_currency='USD', conversion_rates=CONVERSION_RATES, cross_via_matrix=CROSS_VIA_MATRIX):
    try:
        print("From:", from_currency, ' ', amount)
        print("To ", to_currency)
        if from_currency or to_currency != 'JPY':
            if from_currency == to_currency:
                a=round(amount, 2)
                print("= ",to_currency," ", a)
                return a

            if cross_via_matrix[from_currency][to_currency] == 'D':
                b= round(amount * conversion_rates[from_currency + to_currency], 2)
                print("= ",to_currency," ",b)
                return b

            if cross_via_matrix[from_currency][to_currency] == 'Inv':
                c= round(amount / conversion_rates[to_currency + from_currency], 2)
                print("= ",to_currency," ",c)
                return c

            if cross_via_matrix[from_currency][to_currency] == 'EUR':
                d= round(convert_currency(amount, from_currency, 'EUR', conversion_rates, cross_via_matrix) / \
                             convert_currency(1, to_currency, 'EUR', conversion_rates, cross_via_matrix), 2)
                print("= ",to_currency," ",d)
                return d

            if cross_via_matrix[from_currency][to_currency] == 'USD':
                e= round(convert_currency(amount, from_currency, 'USD', conversion_rates, cross_via_matrix) / \
                             convert_currency(1, to_currency, 'USD', conversion_rates, cross_via_matrix), 2)
                print("= ",to_currency," ",e)
                return e

            via_currency = cross_via_matrix[from_currency][to_currency]
            via_amount = convert_currency(amount, from_currency, via_currency, conversion_rates, cross_via_matrix)
            return round(convert_currency(via_amount, via_currency, to_currency, conversion_rates, cross_via_matrix), 2)
        else:
            if from_currency == to_currency:
                a = round(amount, 0)
                print("= ", to_currency, " ", a)
                return a

            if cross_via_matrix[from_currency][to_currency] == 'D':
                b = round(amount * conversion_rates[from_currency + to_currency], 0)
                print("= ", to_currency, " ", b)
                return b

            if cross_via_matrix[from_currency][to_currency] == 'Inv':
                c = round(amount / conversion_rates[to_currency + from_currency], 0)
                print("= ", to_currency, " ", c)
                return c

            if cross_via_matrix[from_currency][to_currency] == 'EUR':
                d = round(convert_currency(amount, from_currency, 'EUR', conversion_rates, cross_via_matrix) / \
                          convert_currency(1, to_currency, 'EUR', conversion_rates, cross_via_matrix), 0)
                print("= ", to_currency, " ", d)
                return d

            if cross_via_matrix[from_currency][to_currency] == 'USD':
                e = round(convert_currency(amount, from_currency, 'USD', conversion_rates, cross_via_matrix) / \
                          convert_currency(1, to_currency, 'USD', conversion_rates, cross_via_matrix), 0)
                print("= ", to_currency, " ", e)
                return e

            via_currency = cross_via_matrix[from_currency][to_currency]
            via_amount = convert_currency(amount, from_currency, via_currency, conversion_rates, cross_via_matrix)
            return round(convert_currency(via_amount, via_currency, to_currency, conversion_rates, cross_via_matrix), 0)
    except KeyError:
        print("Unable to find rate for ", from_currency, '/', to_currency)

def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--amount', type=int, default=1, help='model path or triton URL')
    parser.add_argument('--from_currency', type=str, default='USD' , help='currency')
    parser.add_argument('--to_currency', type=str, default='USD', help='currency')
    opt = parser.parse_args()
    return opt

def main(opt):
    convert_currency(**vars(opt))

if __name__ == '__main__':
    opt = parse_opt()
    main(opt)
