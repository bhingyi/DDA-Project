# Import libraries

from FUN_TEST import *
api_key = '4H4XGZE8HAY85MW6'

def main():
    user = log_in()

    if user:
        while True:
            print("\nOptions:")
            print("1. Deposit Cash")
            print("2. Withdraw Cash")
            print("3. Buy Stocks")
            print("4. Portfolio")
            print("5. View stock data")
            print("6. Stock price comparison")
            print("7. Exit")

            choice = input("Enter your choice (1-7): ")

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
                stock_symbol, stock_price, _ = user.view_stock_data(available_stocks)
                if stock_symbol and stock_price:
                    print(f"Current price of {stock_symbol}: ${stock_price}")

            elif choice == '6':
                user.view_stock_overview(available_stocks)

            elif choice == '7':
                print("Exiting the program. Goodbye!")
                break

            else:
                print("Invalid choice. Please enter a number between 1 and 7.")
