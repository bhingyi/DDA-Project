from CombinedTest import *

users = {'Balazs': UserProfile(username='Balazs', password='Welcome123', initial_cash=10000),
             'Anders': UserProfile(username='Anders', password='Welcome123', initial_cash=15000)}

username = input("Enter your username: ")
user = users[username]

user.portfolio = {'MSFT': 10, 'AAPL': 15, 'GOOGL':5}
prices = [MSFT_price(),AAPL_price(),GOOGL_price()]

user.dataframe = pd.DataFrame.from_dict(user.portfolio,orient='index',columns=['Number of stocks'])
user.dataframe['Value'] = prices * user.dataframe['Number of stocks']


ax = sns.barplot(x=user.dataframe.index, y='Value', data=user.dataframe)
ax.set(xlabel='Stocks', ylabel='Value')
for p in ax.patches:
    ax.text(x=p.get_x() + p.get_width() / 2,
            y=p.get_height(),
            s='${:.2f}'.format(p.get_height()),
            ha='center')
# Show the plot
plt.show()
