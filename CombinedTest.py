import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#Defining API key as global variable
api_key = '4H4XGZE8HAY85MW6'

class UserProfile:
    def __init__(self, username, password, initial_cash):
        self.username = username
        self.password = password
        self.cash_balance = initial_cash
        self.portfolio = {'MSFT': 0, 'AAPL': 0, 'GOOGL':0}#{} #we should set the dict kys in a fixed order or our stocks
        self.dataframe = pd.DataFrame()

    def deposit_cash(self, amount):
        self.cash_balance += amount
        return f"Deposited ${amount}. New cash balance: ${self.cash_balance}"

    def withdraw_cash(self, amount):
        if amount > self.cash_balance:
            return "Insufficient funds for withdrawal"
        self.cash_balance -= amount
        return f"Withdrew ${amount}. New cash balance: ${self.cash_balance}"

    def buy_stock(self, symbol, quantity, stock_price):
        cost = quantity * stock_price
        if cost > self.cash_balance:
            return "Insufficient funds"
        self.cash_balance -= cost
        if symbol in self.portfolio:
            self.portfolio[symbol]['quantity'] += quantity
        else:
            self.portfolio[symbol] = {'quantity': quantity, 'stock_price': stock_price}

        return f"Bought {quantity} shares of {symbol} for ${cost}. New cash balance: ${self.cash_balance}"

    def sell_stock(self, symbol, quantity, stock_price):
        if symbol not in self.portfolio or self.portfolio[symbol]['quantity'] < quantity:
            return "Not enough stocks to sell"

        revenue = quantity * stock_price
        self.cash_balance += revenue
        self.portfolio[symbol]['quantity'] -= quantity

        if self.portfolio[symbol]['quantity'] == 0:
            del self.portfolio[symbol]

        return f"Sold {quantity} shares of {symbol} for ${revenue}. New cash balance: ${self.cash_balance}"

    def portfolio_summary(self):
        summary = []
        for symbol, details in self.portfolio.items():
            quantity = details['quantity']
            stock_price = details['stock_price']
            total_worth = quantity * stock_price
            summary.append(f"{symbol}: Quantity - {quantity}, Stock Price - ${stock_price}, Total Worth - ${total_worth}")
        return summary

    def visual_summary(self):
        prices = [MSFT_price(), AAPL_price(), GOOGL_price()]
        self.dataframe = pd.DataFrame.from_dict(self.portfolio, orient='index', columns=['Number of stocks'])
        self.dataframe['Value'] = prices * self.dataframe['Number of stocks']

        ax = sns.barplot(x=self.dataframe.index, y='Value', data=self.dataframe, palette=['b', 'g', 'r', 'c'])
        ax.set_xlabel('Stocks', weight='bold', fontsize=14)
        ax.set_ylabel('Value', weight='bold', fontsize=14)
        for p in ax.patches:
            ax.text(x=p.get_x() + p.get_width() / 2,
                    y=p.get_height(),
                    s='${:.2f}'.format(p.get_height()),
                    ha='center',
                    weight='bold',
                    fontsize=14)
        ax.set_title(f'Value of portfolio at {last_time_stamp('MSFT',api_key)}', weight='bold', fontsize=18)
        # Show the plot
        plt.show()


    def view_portfolio(self):
        summary = self.portfolio_summary()
        if summary:
            print("\nPortfolio Summary:")
            for item in summary:
                print(item)
        else:
            print("No stocks in the portfolio.")

    def view_stock_data(self, available_stocks):
        print("\nAvailable stocks with prices:")
        for stock, price in available_stocks.items():
            print(f"- {stock}: ${price}")

        stock_symbol = input("Enter the stock symbol you want to view data (type 'NVM' to go back): ")

        if stock_symbol.upper() == 'NVM':
            return None, None, None

        if stock_symbol not in available_stocks:
            print("Invalid stock symbol.")
            return None, None, None

        endpoint = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={stock_symbol}&interval=1min&outputsize=full&apikey={api_key}"

        response = requests.get(endpoint)

        if response.status_code != 200:
            print(f"Could not retrieve data for {stock_symbol}, code: {response.status_code}")
            return None, None, None

        raw_data = response.json()
        time_series = raw_data.get('Time Series (1min)')

        if not time_series:
            print(f"No time series data found for {stock_symbol}")
            return None, None, None

        data = pd.DataFrame(time_series).T.apply(pd.to_numeric)
        data.index = pd.DatetimeIndex(data.index)
        data.rename(columns=lambda s: s[3:], inplace=True)

        plt.figure(figsize=(12, 6))
        sns.lineplot(data=data[['open', 'high', 'low', 'close']])
        plt.title(f"Stock Data for {stock_symbol}")
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.show()

        return stock_symbol, data['close'].iloc[-1], None


# Functions to get the latest stock prices for the available stocks (defiend by us): currently Apple, Google and Microsoft
def AAPL_price():
    symbol = 'AAPL'
    endpoint = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=1min&outputsize=full&apikey={api_key}"

    response = requests.get(endpoint)

    if response.status_code != 200:
        return f"Could not retrieve data for {symbol}, code: {response.status_code}", None

    raw_data = response.json()
    time_series = raw_data.get('Time Series (1min)')

    if not time_series:
        return f"No time series data found for {symbol}", None

    data = pd.DataFrame(time_series).T.apply(pd.to_numeric)
    data.index = pd.DatetimeIndex(data.index)
    data.rename(columns=lambda s: s[3:], inplace=True)

    # Extract the latest stock price
    price_AAPL = data['close'].iloc[-1]

    return price_AAPL

def GOOGL_price():
    symbol = 'GOOGL'
    endpoint = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=1min&outputsize=full&apikey={api_key}"

    response = requests.get(endpoint)

    if response.status_code != 200:
        return f"Could not retrieve data for {symbol}, code: {response.status_code}", None

    raw_data = response.json()
    time_series = raw_data.get('Time Series (1min)')

    if not time_series:
        return f"No time series data found for {symbol}", None

    data = pd.DataFrame(time_series).T.apply(pd.to_numeric)
    data.index = pd.DatetimeIndex(data.index)
    data.rename(columns=lambda s: s[3:], inplace=True)

    # Extract the latest stock price
    price_GOOGL = data['close'].iloc[-1]

    return price_GOOGL

def MSFT_price():
    symbol = 'MSFT'
    endpoint = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=1min&outputsize=full&apikey={api_key}"

    response = requests.get(endpoint)

    if response.status_code != 200:
        return f"Could not retrieve data for {symbol}, code: {response.status_code}", None

    raw_data = response.json()
    time_series = raw_data.get('Time Series (1min)')

    if not time_series:
        return f"No time series data found for {symbol}", None

    data = pd.DataFrame(time_series).T.apply(pd.to_numeric)
    data.index = pd.DatetimeIndex(data.index)
    data.rename(columns=lambda s: s[3:], inplace=True)

    # Extract the latest stock price
    price_MSFT = data['close'].iloc[-1]

    return price_MSFT

def last_time_stamp(symbol, api_key):
    endpoint = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=1min&outputsize=full&apikey={api_key}"

    response = requests.get(endpoint)

    # Since we are retrieving stuff from a web service, it's a good idea to check for the return status code
    if response.status_code != 200:
        raise ValueError("Could not retrieve data, code:", response.status_code)

    # The service sends JSON data, we parse that into a Python datastructure
    raw_data = response.json()

    # Creating data frame
    data = raw_data['Time Series (1min)']
    df_data = pd.DataFrame(data).T.apply(pd.to_numeric)

    # Next we parse the index to create a datetimeindex
    df_data.index = pd.DatetimeIndex(df.index)

    # Let's fix the column names by chopping off the first 3 characters
    df_data.rename(columns=lambda s: s[3:], inplace=True)
    last_time_stamp = df_data.index[0]

    return last_time_stamp


def log_in():
    users = {'Balazs': UserProfile(username='Balazs', password='Welcome123', initial_cash=10000),
             'Anders': UserProfile(username='Anders', password='Welcome123', initial_cash=15000)}

    while True:
        username = input("Enter your username: ")

        if username not in users:
            print("User not found.")
            continue

        user = users[username]

        # Ask for password
        password_attempt = input("Enter your password: ")

        if password_attempt != user.password:
            print("Incorrect password. Please try again.")
            continue

        print(f"Welcome, {user.username}!")
        print(f"Current cash balance: ${user.cash_balance}")
        return user

def sell_stocks_menu(user):
    print("\nSell Stocks Menu:")
    print("Select the stock you want to sell (type 'NVM' to go back):")
    portfolio_summary = user.portfolio_summary()
    for i, item in enumerate(portfolio_summary, 1):
        print(f"{i}. {item}")

    choice = input("Enter the number corresponding to the stock you want to sell: ")

    if choice.upper() == 'NVM':
        return None, None, None

    try:
        choice_index = int(choice) - 1
        if 0 <= choice_index < len(portfolio_summary):
            selected_stock = portfolio_summary[choice_index]
            stock_symbol = selected_stock.split(":")[0].strip()
            quantity = int(input(f"Enter the quantity you want to sell for {stock_symbol}: "))
            stock_price = user.portfolio[stock_symbol]['stock_price']
            return stock_symbol, stock_price, quantity
        else:
            print("Invalid choice.")
    except ValueError:
        print("Invalid input. Please enter a number.")

    return None, None, None

def portfolio_menu(user):
    print("\nPortfolio Menu:")
    print("1. View Owned Stocks")
    print("2. Sell a Stock")
    print("3. Back to Main Menu")

    choice = input("Enter your choice (1-3): ")

    if choice == '1':
        user.view_portfolio()

    elif choice == '2':
        stock_symbol, stock_price, quantity = sell_stocks_menu(user)
        if stock_symbol and stock_price and quantity:
            print(user.sell_stock(symbol=stock_symbol, quantity=quantity, stock_price=stock_price))

    elif choice == '3':
        print("Returning to the main menu.")

    else:
        print("Invalid choice. Please enter a number between 1 and 3.")

def main():
    user = log_in()

    if user:
        available_stocks = {'AAPL': AAPL_price(), 'GOOGL': GOOGL_price(), 'MSFT': MSFT_price()}

        while True:
            print("\nOptions:")
            print("1. Deposit Cash")
            print("2. Withdraw Cash")
            print("3. Portfolio")
            print("4. View Stock Data")
            print("5. Buy Stocks")
            print("6. Exit")

            choice = input("Enter your choice (1-6): ")

            if choice == '1':
                amount = float(input("Enter the amount to deposit: "))
                print(user.deposit_cash(amount))

            elif choice == '2':
                amount = float(input("Enter the amount to withdraw: "))
                print(user.withdraw_cash(amount))

            elif choice == '3':
                portfolio_menu(user)

            elif choice == '4':
                stock_symbol, stock_price, _ = user.view_stock_data(available_stocks)
                if stock_symbol and stock_price:
                    print(f"Current price of {stock_symbol}: ${stock_price}")

            elif choice == '5':
                print("\nAvailable stocks with prices:")
                for stock, price in available_stocks.items():
                    print(f"- {stock}: ${price}")

                stock_symbol = input("Enter the stock symbol you want to buy (type 'NVM' to go back): ")

                if stock_symbol.upper() == 'NVM':
                    continue

                if stock_symbol not in available_stocks:
                    print("Invalid stock symbol.")
                    continue

                quantity = int(input("Enter the quantity you want to buy: "))

                if quantity <= 0:
                    print("Quantity must be greater than zero.")
                    continue

                stock_price = available_stocks[stock_symbol]
                total_amount = quantity * stock_price

                print(f"Total amount for {quantity} shares of {stock_symbol}: ${total_amount}")

                confirmation = input("Do you want to proceed with the purchase? (Y/N): ").upper()

                if confirmation == 'Y':
                    print(user.buy_stock(symbol=stock_symbol, quantity=quantity, stock_price=stock_price))
                elif confirmation == 'N':
                    print("Purchase canceled.")
                else:
                    print("Invalid choice. Please enter 'Y' or 'N'.")

            elif choice == '6':
                print("Exiting the program. Goodbye!")
                break

            else:
                print("Invalid choice. Please enter a number between 1 and 6.")

if __name__ == "__main__":
    main()
