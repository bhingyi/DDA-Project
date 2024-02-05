# Import libraries
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

api_key = '4H4XGZE8HAY85MW6'

# Functions to get the latest stock prices for the available stocks (defiend by us): currently Apple, Google and Microsoft
def AAPL_data():
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

    return data

def AAPL_price():

    # Extract the latest stock price
    price_AAPL = AAPL_data()['close'].iloc[-1]

    return price_AAPL

def GOOGL_data():
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

    return data

def GOOGL_price():
    # Extract the latest stock price
    price_GOOGL = GOOGL_data()['close'].iloc[-1]

    return price_GOOGL


def MSFT_data():
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

    return data

def MSFT_price():
    # Extract the latest stock price
    price_MSFT = MSFT_data()['close'].iloc[-1]

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
    df_data.index = pd.DatetimeIndex(df_data.index)

    # Let's fix the column names by chopping off the first 3 characters
    df_data.rename(columns=lambda s: s[3:], inplace=True)
    last_time_stamp = df_data.index[0]

    return last_time_stamp


