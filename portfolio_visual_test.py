import read_stock_prices
from CombinedTest import *
from read_stock_prices import last_time_stamp


users = {'Balazs': UserProfile(username='Balazs', password='Welcome123', initial_cash=10000),
             'Anders': UserProfile(username='Anders', password='Welcome123', initial_cash=15000)}

username = input("Enter your username: ")
user = users[username]

user.portfolio = {'MSFT': 10, 'AAPL': 15, 'GOOGL':5}
prices = [MSFT_price(),AAPL_price(),GOOGL_price()]

user.dataframe = pd.DataFrame.from_dict(user.portfolio,orient='index',columns=['Number of stocks'])
user.dataframe['Value'] = prices * user.dataframe['Number of stocks']


ax = sns.barplot(x=user.dataframe.index, y='Value', data=user.dataframe, palette=['b', 'g', 'r', 'c'])
ax.set_xlabel('Stocks', weight='bold', fontsize=14)
ax.set_ylabel('Value', weight='bold', fontsize=14)
for p in ax.patches:
    ax.text(x=p.get_x() + p.get_width() / 2,
            y=p.get_height(),
            s='${:.2f}'.format(p.get_height()),
            ha='center',
            weight='bold',
            fontsize=14)
ax.set_title(f'Value of portfolio at TIME', weight='bold', fontsize=18)
# Show the plot
plt.show()
