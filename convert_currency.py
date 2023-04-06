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
'AUD': {'AUD': '1', 'CAD': 'USD', 'CNY': 'USD', 'CZK': 'USD', 'DKK': 'USD', 'EUR': 'USD', 'GBP': 'USD', 'JPY': 'USD', 'NOK': 'USD', 'NZD': 'USD', 'USD': 'D'},
'CAD': {'AUD': 'USD', 'CAD': '1', 'CNY': 'USD', 'CZK': 'USD', 'DKK': 'USD', 'EUR': 'USD', 'GBP': 'USD', 'JPY': 'USD', 'NOK': 'USD', 'NZD': 'USD', 'USD': 'D'},
'CNY': {'AUD': 'USD', 'CAD': 'USD', 'CNY': '1', 'CZK': 'USD', 'DKK': 'USD', 'EUR': 'USD', 'GBP': 'USD', 'JPY': 'USD', 'NOK': 'USD', 'NZD': 'USD', 'USD': 'D'},
'CZK': {'AUD': 'USD', 'CAD': 'USD', 'CNY': 'USD', 'CZK': '1', 'DKK': 'EUR', 'EUR': 'Inv', 'GBP': 'USD', 'JPY': 'USD', 'NOK': 'EUR', 'NZD': 'USD', 'USD': 'EUR'},
'DKK': {'AUD': 'USD', 'CAD': 'USD', 'CNY': 'USD', 'CZK': 'EUR', 'DKK': '1', 'EUR': 'Inv', 'GBP': 'USD', 'JPY': 'USD', 'NOK': 'EUR', 'NZD': 'USD', 'USD': 'EUR'},
'EUR': {'AUD': 'USD', 'CAD': 'USD', 'CNY': 'USD', 'CZK': 'D', 'DKK': 'D', 'EUR': '1', 'GBP': 'USD', 'JPY': 'USD', 'NOK': 'USD', 'NZD': 'USD', 'USD': 'USD'},
'GBP': {'AUD': 'USD', 'CAD': 'USD', 'CNY': 'USD', 'CZK': 'USD', 'DKK': 'USD', 'EUR': 'USD', 'GBP': '1', 'JPY': 'USD', 'NOK': 'USD', 'NZD': 'USD', 'USD': 'D'},
'JPY': {'AUD': 'USD', 'CAD': 'USD', 'CNY': 'USD', 'CZK': 'USD', 'DKK': 'USD', 'EUR': 'USD', 'GBP': 'USD', 'JPY': '1', 'NOK': 'USD', 'NZD': 'USD', 'USD': 'Inv'},
'NOK': {'AUD': 'USD', 'CAD': 'USD', 'CNY': 'USD', 'CZK': 'EUR', 'DKK': 'EUR', 'EUR': 'Inv', 'GBP': 'USD', 'JPY': 'USD', 'NOK': '1', 'NZD': 'USD', 'USD': 'EUR'},
'NZD': {'AUD': 'USD', 'CAD': 'USD', 'CNY': 'USD', 'CZK': 'USD', 'DKK': 'USD', 'EUR': 'USD', 'GBP': 'USD', 'JPY': 'USD', 'NOK': 'USD', 'NZD': '1', 'USD': 'D'},
'USD': {'AUD': 'Inv', 'CAD': 'Inv', 'CNY': 'Inv', 'CZK': 'EUR', 'DKK': 'EUR', 'EUR': 'Inv', 'GBP': 'Inv', 'JPY': 'D', 'NOK': 'EUR', 'NZD': 'Inv', 'USD': '1'}
}

def convert_currency(amount, from_currency, to_currency, conversion_rates, cross_via_matrix):
    try:
        print("From:",from_currency,' ',amount)
        print("To ",to_currency)
        if from_currency == to_currency:
            return round(amount,2)

        if cross_via_matrix[from_currency][to_currency] == 'D':
            return round(amount * conversion_rates[from_currency + to_currency],2)

        if cross_via_matrix[from_currency][to_currency] == 'Inv':
            return round(amount / conversion_rates[to_currency + from_currency],2)

        if cross_via_matrix[from_currency][to_currency] == 'EUR':
            return round(convert_currency(amount, from_currency, 'EUR', conversion_rates, cross_via_matrix) / \
                convert_currency(1,to_currency,'EUR',conversion_rates,cross_via_matrix),2)

        if cross_via_matrix[from_currency][to_currency] == 'USD':
            return round(convert_currency(amount, from_currency, 'USD', conversion_rates, cross_via_matrix) / \
                convert_currency(1,to_currency,'USD',conversion_rates,cross_via_matrix),2)

        via_currency = cross_via_matrix[from_currency][to_currency]
        via_amount = convert_currency(amount, from_currency, via_currency, conversion_rates, cross_via_matrix)
        return round(convert_currency(via_amount, via_currency, to_currency, conversion_rates, cross_via_matrix),2)
    except KeyError as e:
        print(f"Unable to find rate for ",from_currency, to_currency)
        
  # to test
print(convert_currency(1, 'AUD', 'USD', CONVERSION_RATES, CROSS_VIA_MATRIX)) # given 83.71  OUTPUT 83.71
print(convert_currency(1, 'USD', 'AUD', CONVERSION_RATES, CROSS_VIA_MATRIX)) # given 1.1946 OUTPUT 1.1946004061641382
print(convert_currency(1, 'AUD', 'JPY', CONVERSION_RATES, CROSS_VIA_MATRIX)) # given  100.41 OUTPUT 100.41014499999999
print(convert_currency(1, 'USD', 'USD', CONVERSION_RATES, CROSS_VIA_MATRIX)) # given  1 OUTPUT 1
print(convert_currency(1, 'ABC', 'USD', CONVERSION_RATES, CROSS_VIA_MATRIX)) # given "Unable to find rate for KRW/FJD" OUTPUT Unable to find rate for  ABC USD
