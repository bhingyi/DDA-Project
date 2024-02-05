# Import libraries
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from DATA_FUNC_TEST import *

api_key = '4H4XGZE8HAY85MW6'

#Define class for user profile
class UserProfile:
    # Initialize user profile with username, password, and initial cash
    def __init__(self, username, password, initial_cash):
        self.username = username
        self.password = password
        self.cash_balance = initial_cash
        self.portfolio = {}
        self.dataframe = pd.DataFrame.from_dict({'MSFT': 0, 'AAPL': 0, 'GOOGL':0}, orient='index', columns=['Number of stocks'])

    # Method to deposit cash into the user's account
    def deposit_cash(self, amount):
        self.cash_balance += amount
        return f"Deposited ${amount}. New cash balance: ${self.cash_balance}"

    # Method to withdraw cash from the user's account
    def withdraw_cash(self, amount):
        if amount > self.cash_balance:
            return "Insufficient funds for withdrawal"
        self.cash_balance -= amount
        return f"Withdrew ${amount}. New cash balance: ${self.cash_balance}"

    # Method to buy stocks
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

    # Method to sell stocks
    def sell_stock(self, symbol, quantity, stock_price):
        if symbol not in self.portfolio or self.portfolio[symbol]['quantity'] < quantity:
            return "Not enough stocks to sell"

        revenue = quantity * stock_price
        self.cash_balance += revenue
        self.portfolio[symbol]['quantity'] -= quantity

        if self.portfolio[symbol]['quantity'] == 0:
            del self.portfolio[symbol]

        return f"Sold {quantity} shares of {symbol} for ${revenue}. New cash balance: ${self.cash_balance}"

    # Method to generate a summary of the user's portfolio
    def portfolio_summary(self):
        summary = []
        for symbol, details in self.portfolio.items():
            quantity = details['quantity']
            stock_price = details['stock_price']
            total_worth = quantity * stock_price
            summary.append(f"{symbol}: Quantity: {quantity}, Stock Price: ${stock_price}, Total Worth: ${total_worth}")
            self.dataframe[symbol, 'Number of stocks'] = quantity
            self.dataframe[symbol, 'Value'] = total_worth
        return summary

    def portfolio_dict(self):
        p_dict = {'MSFT': 0, 'AAPL': 0, 'GOOGL':0}
        for symbol, details in self.portfolio.items():
            quantity = details['quantity']
            stock_price = details['stock_price']
            total_worth = quantity * stock_price
            p_dict[symbol] = total_worth
        return p_dict

    #Method to generate plot for portfolio overview
    def visual_summary(self):
        prices = [MSFT_price(), AAPL_price(), GOOGL_price()]
        self.dataframe = pd.DataFrame.from_dict(self.portfolio_dict(), orient='index', columns=['Value'])

        ax = sns.barplot(x=self.dataframe.index, y='Value', hue=self.dataframe.index, data=self.dataframe, palette=['b', 'g', 'r'])
        ax.set_xlabel('Stocks', weight='bold', fontsize=14)
        ax.set_ylabel('Value', weight='bold', fontsize=14)
        for p in ax.patches:
            ax.text(x=p.get_x() + p.get_width() / 2,
                    y=p.get_height(),
                    s='${:.2f}'.format(p.get_height()),
                    ha='center',
                    weight='bold',
                    fontsize=14)
        ax.set_title(f'Total value of portfolio: $ {sum(self.dataframe['Value'])}', weight='bold', fontsize=18)
        # Show the plot
        plt.show()

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

    def view_stock_overview(self, available_stocks):
        print("\nAvailable stocks with prices:")
        for stock, price in available_stocks.items():
            print(f"- {stock}: ${price}")

        apple_close = pd.DataFrame(AAPL_data()['close']).rename(columns={'close' :'Apple'})
        msft_close = pd.DataFrame(MSFT_data()['close']).rename(columns={'close' :'Microsoft'})
        google_close = pd.DataFrame(GOOGL_data()['close']).rename(columns={'close' :'Google'})

        data = pd.concat([apple_close,msft_close,google_close], axis = 1)

        plt.figure(figsize=(12, 6))
        ax = sns.lineplot(data=data[['Apple', 'Microsoft', 'Google']])
        plt.title(f"Stock price development")
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.show()

        return ax


