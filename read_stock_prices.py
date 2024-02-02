import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


#Main part, to be used in the other script as well
symbol = input('Choose stock:')
api_key = '1N6YRB5DJEH8E7HP'
endpoint = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=5min&outputsize=full&apikey={api_key}"

response = requests.get(endpoint)

# Since we are retrieving stuff from a web service, it's a good idea to check for the return status code
if response.status_code != 200:
    raise ValueError("Could not retrieve data, code:", response.status_code)

# The service sends JSON data, we parse that into a Python datastructure
raw_data = response.json()

# The other key/value pair is the actual time series.
# This is a dict as well
time_series = raw_data['Time Series (5min)']

#Creating data frame
data = raw_data['Time Series (5min)']
df = pd.DataFrame(data).T.apply(pd.to_numeric)
df.info()
df.head()

# Next we parse the index to create a datetimeindex
df.index = pd.DatetimeIndex(df.index)

# Let's fix the column names by chopping off the first 3 characters
df.rename(columns=lambda s: s[3:], inplace=True)

# Let's take last value of the close column for every business day
close_per_day = df.close.resample('B').last()
# Getting opening value every business day
open_per_day = df.open.resample('B').first()

# Getting lowest value for every business day
low_per_day = df.low.resample('B').min()

# Getting highest value for every business day
high_per_day = df.high.resample('B').max()

df_per_day = pd.concat([open_per_day, low_per_day, high_per_day, close_per_day], axis=1)

# Dates to a variable
dates = close_per_day.index



#Exploring data and testing plots

if __name__ == '__main__':

    api_key = '1N6YRB5DJEH8E7HP'
    endpoint = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=5min&outputsize=full&apikey={api_key}"

    response = requests.get(endpoint)

    # Since we are retrieving stuff from a web service, it's a good idea to check for the return status code
    # See: https://en.wikipedia.org/wiki/List_of_HTTP_status_codes
    if response.status_code != 200:
        raise ValueError("Could not retrieve data, code:", response.status_code)

    # The service sends JSON data, we parse that into a Python datastructure
    raw_data = response.json()

    # Let's look at the raw data
    type(raw_data)

    # So it's a dict. what are the keys?
    raw_data.keys()

    # Let's look at the first key/value.
    # This is just some descriptive information
    raw_data['Meta Data']
    #Microsoft stocks

    # The other key/value pair is the actual time series.
    # This is a dict as well
    time_series = raw_data['Time Series (5min)']
    type(time_series)

    # How many items are in there?
    len(time_series)

    # How many items are in there?
    len(time_series)

    # Let's take the first few keys
    first_ten_keys = list(time_series.keys())[:10]
    # And see the corresponding values
    first_ten_items = [f"{key}: {time_series[key]}" for key in first_ten_keys ]
    print("\n".join(first_ten_items))

    #### Creating dataframe ###

    data = raw_data['Time Series (5min)']
    df = pd.DataFrame(data).T.apply(pd.to_numeric)
    df.info()
    df.head()

    # Next we parse the index to create a datetimeindex
    df.index = pd.DatetimeIndex(df.index)

    # Let's fix the column names by chopping off the first 3 characters
    df.rename(columns=lambda s: s[3:], inplace=True)

    #df.info()
    #df.head()

    df[['open', 'high', 'low', 'close']].plot()

    plt.figure(figsize=(12,6))
    sns.lineplot(data=df[['open', 'high', 'low', 'close']])
    plt.title("What's in the data?")
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.show()

    #Volume traded per day
    plt.figure(figsize=(12,6))
    sns.lineplot(data=df[['volume']])
    plt.title("Volume traded per day")
    plt.xlabel('Date')
    plt.ylabel('Volume')
    plt.show()


    #### Resampling ###

    # Let's take last value of the close column for every business day
    close_per_day = df.close.resample('B').last()

    plt.figure(figsize=(12,6))
    sns.lineplot(x=close_per_day.index, y=close_per_day.values)
    plt.title('Close per Day')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.show()

    # Getting opening value every business day
    open_per_day = df.open.resample('B').first()

    # Getting lowest value for every business day
    low_per_day = df.low.resample('B').min()

    # Getting highest value for every business day
    high_per_day = df.high.resample('B').max()

    df_per_day = pd.concat([open_per_day,low_per_day,high_per_day,close_per_day], axis=1)
    print(df_per_day)


    plt.figure(figsize=(12,6))
    sns.lineplot(data=df_per_day[['open', 'high', 'low', 'close']])
    plt.title("Only daily data")
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.show()

    #Dates to a variable
    dates = close_per_day.index

    #orig data plot
    plt.figure(figsize=(12,6))
    sns.lineplot(data=df[['open', 'high', 'low', 'close']])
    plt.title("What's in the data?")
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.show()

    #daily data plot
    sns.set_style('darkgrid')
    plt.figure(figsize=(12,6))
    sns.lineplot(data=df_per_day[['open', 'high', 'low', 'close']])
    plt.title("Only daily data")
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.show()
