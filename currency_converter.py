def get_amount():
    while True:
        try:
            amount = float(input('Enter the amount: '))
            if amount <= 0:
                raise ValueError()
            return amount
        except ValueError:
            print('Invalid amount')


def get_currency(label):
    currencies = ('USD', 'EUR', 'CAD')
    while True:
        currency = input(f'{label} currency (USD/EUR/CAD): ').upper()
        if currency not in currencies:
            print('Invalid currency')
        else:
            return currency


def convert(amount, source_currency, target_currency):
    exchange_rates = {
        'USD': {'EUR': 0.85, 'CAD': 1.25},
        'EUR': {'USD': 1.18, 'CAD': 1.47},
        'CAD': {'USD': 0.80, 'EUR': 0.68},
    }

    if source_currency == target_currency:
        return amount

    return amount * exchange_rates[source_currency][target_currency]


def convert_all(amount, source_currency):
    exchange_rates = {
        'USD': {'EUR': 0.85, 'CAD': 1.25},
        'EUR': {'USD': 1.18, 'CAD': 1.47},
        'CAD': {'USD': 0.80, 'EUR': 0.68},
    }

    conversions = {}
    for currency, rate in exchange_rates[source_currency].items():
        conversions[currency] = round(amount * rate, 2)

    return conversions


def main():
    conversion_history = []

    while True:
        result = input("Do you want to continue? (y/n) ").lower()

        if result == 'n':
            print("Conversion History:")
            for entry in conversion_history:
                print(entry)
            break

        amount = get_amount()
        source_currency = get_currency('Source')
        target_currency = get_currency('Target')

        converted_amount = convert(amount, source_currency, target_currency)
        print(
            f'{amount} {source_currency} is equal to {converted_amount:.2f} {target_currency}')
        print("-" * 33)

        conversion_history.append(
            {source_currency: amount, target_currency: round(converted_amount, 2)})

        conversions = convert_all(amount, source_currency)
        for currency, value in conversions.items():
            print(f'{amount} {source_currency} is equal to {value} {currency}')


if __name__ == "__main__":
    main()
