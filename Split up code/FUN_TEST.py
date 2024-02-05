# Import libraries

from DATA_FUNC_TEST import *
from U_CLASS_TEST import UserProfile

api_key = '4H4XGZE8HAY85MW6'

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

available_stocks = {'AAPL': AAPL_price(), 'GOOGL': GOOGL_price(), 'MSFT': MSFT_price()}
# Function to handle buying stocks
def buy_stocks_menu():
    while True:
        # Display available stocks with prices
        available_stocks = {'AAPL': AAPL_price(), 'GOOGL': GOOGL_price(), 'MSFT': MSFT_price()}
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
        user.visual_summary()
        #print(user.portfolio_dict())
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
