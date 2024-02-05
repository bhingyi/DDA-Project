
# Import libraries
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


#Define class for user profile
class UserProfile:
    # Initialize user profile with username, password, and initial cash
    def __init__(self, username, password, initial_cash):
        self.username = username
        self.password = password
        self.cash_balance = initial_cash
        self.portfolio = {}

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
            summary.append(f"{symbol}: Quantity - {quantity}, Stock Price - ${stock_price}, Total Worth - ${total_worth}")
        return summary

# Function to handle user login
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


# Function to handle buying stocks
def buy_stocks_menu():
    while True:
        # Display available stocks with prices
        available_stocks = {'AAPL': 150.50, 'GOOGL': 1200.75, 'MSFT': 300.20}
        print("\nAvailable stocks with prices:")
        for stock, price in available_stocks.items():
            print(f"- {stock}: ${price}")

        stock_symbol = input("Enter the stock symbol you want to buy (type 'NVM' to go back): ")

        if stock_symbol.upper() == 'NVM':
            return None, None, None

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
            return stock_symbol, stock_price, quantity
        elif confirmation == 'N':
            print("Purchase canceled.")
            continue
        else:
            print("Invalid choice. Please enter 'Y' or 'N'.")

# Function to handle selling stocks
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

# Function to handle portfolio-related menu options
def portfolio_menu(user):
    print("\nPortfolio Menu:")
    print("1. View Owned Stocks")
    print("2. Buy More of a Stock")
    print("3. Sell a Stock")
    print("4. Back to Main Menu")

    choice = input("Enter your choice (1-4): ")

    if choice == '1':
        portfolio_summary = user.portfolio_summary()
        if portfolio_summary:
            print("\nPortfolio Summary:")
            for item in portfolio_summary:
                print(item)
        else:
            print("No stocks in the portfolio.")

    elif choice == '2':
        stock_symbol, stock_price, quantity = buy_stocks_menu()
        if stock_symbol and stock_price and quantity:
            print(user.buy_stock(symbol=stock_symbol, quantity=quantity, stock_price=stock_price))

    elif choice == '3':
        stock_symbol, stock_price, quantity = sell_stocks_menu(user)
        if stock_symbol and stock_price and quantity:
            print(user.sell_stock(symbol=stock_symbol, quantity=quantity, stock_price=stock_price))

    elif choice == '4':
        print("Returning to the main menu.")

    else:
        print("Invalid choice. Please enter a number between 1 and 4.")


def main():
    user = log_in()

    if user:
        while True:
            print("\nOptions:")
            print("1. Deposit Cash")
            print("2. Withdraw Cash")
            print("3. Buy Stocks")
            print("4. Portfolio")
            print("5. Exit")

            choice = input("Enter your choice (1-5): ")

            if choice == '1':
                amount = float(input("Enter the amount to deposit: "))
                print(user.deposit_cash(amount))

            elif choice == '2':
                amount = float(input("Enter the amount to withdraw: "))
                print(user.withdraw_cash(amount))

            elif choice == '3':
                stock_symbol, stock_price, quantity = buy_stocks_menu()
                if stock_symbol and stock_price and quantity:
                    print(user.buy_stock(symbol=stock_symbol, quantity=quantity, stock_price=stock_price))

            elif choice == '4':
                portfolio_menu(user)

            elif choice == '5':
                print("Exiting the program. Goodbye!")
                break

            else:
                print("Invalid choice. Please enter a number between 1 and 5.")


if __name__ == "__main__":
    main()
