import streamlit as st
from datetime import date
import datetime as dt
import yfinance as fyf
import yahoo_fin.stock_info as si
from pandas_datareader import data as pdr
import talib
import pandas as pd
import datetime
import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.stats import norm
import math
import plotly.figure_factory as ff
import copy
import ssl
import plotly.graph_objects as go
ssl._create_default_https_context = ssl._create_unverified_context

st.title("PE Bell Curve")

# start of the FrontEnd
def main():
    """Runs the main user interface """
    # header = st.container()
    features = st.container()


    # with header:
    #     st.title('QuantStacks Prototype')
    #     st.text('Evaluate undervalued or overvalued stock.')

    with features:
        global ticker, start, end
        ticker =  st.text_input('Enter Desired Ticker')
        start = st.date_input("Enter Starting Date", datetime.date(1950,1,1)) # create start date input box, set '2020-02-11' = default
        today = date.today().strftime("%Y-%m-%d")
        end = st.text_input("End Date", f'{today}') # create end date input box, set today = default
        

        ticker = ticker.upper()
        if not ticker:
            st.info('Please input a valid ticker')
        else:
            st.success('You selected ticker: {}'.format(ticker))
            with st.spinner('Loading data......'):
                setup()
                OHLC_original = grab_OHLC(ticker)
                Earnings = grab_historical_EPS(ticker)
                #deepcopy OHLC to access full volume and volatility
                OHLC = copy.deepcopy(OHLC_original)

                edit_EPS(ticker,Earnings)
                Merged = merge_OHLC_EPS_ttm(ticker, OHLC, Earnings)
                #get PE only for the dates that have earnings
                calc_PE_ratio(ticker,Merged)
                #get Volatility of the full historical data
                calc_volatility(ticker,OHLC_original)

                st.header('PE ratio probability curve')
                PE_stats = get_PE_stats(ticker,Merged)
                PE_CDF = get_CDF(PE_stats)
                st.subheader("Risk for {} is {}".format(ticker,PE_CDF))
                suggestion(PE_CDF,"PE")
                normal_distribution_curve(PE_stats,"PE Ratio")

                st.header('Buy and Sell Signals')
                morning_star = talib.CDLMORNINGSTAR(Historical_Prices['Open'], Historical_Prices['High'], Historical_Prices['Low'], Historical_Prices['Close'])
                engulfing = talib.CDLENGULFING(Historical_Prices['Open'], Historical_Prices['High'], Historical_Prices['Low'], Historical_Prices['Close'])
                Historical_Prices['Morning Star'] = morning_star
                Historical_Prices['Engulfing'] = engulfing
                engulfing_buy_days = Historical_Prices[Historical_Prices['Engulfing'] ==100]
                engulfing_sell_days = Historical_Prices[Historical_Prices['Engulfing'] ==-100]
                st.write('Buy Days')
                st.write(engulfing_buy_days.tail(3))
                st.write('Sell Days')
                st.write(engulfing_sell_days.tail(3))
                
                st.header('Volatility curve')
                volatility_stats = get_volatility_stats(ticker,OHLC_original)
                volatility_CDF = get_CDF(volatility_stats)
                st.subheader("The CDF of the Volatility for {} is {}".format(ticker,volatility_CDF))
                suggestion(volatility_CDF,"Volatility")
                normal_distribution_curve(volatility_stats,"Volatility")

                st.header('Volume curve')
                volume_stats = get_volume_stats(ticker,OHLC_original)
                volume_CDF = get_CDF(volume_stats)
                st.subheader("The CDF of the Volume for {} is {}".format(ticker,volume_CDF))
                suggestion(volume_CDF,"Volume")
                normal_distribution_curve(volume_stats,"Volume")

            st.success('Done!')

def setup():
    """ Create necessary global variables, gets current directory and create path where all files will be downloaded to """
    # local file locations
    cwd = os.getcwd()
    global path
    path = cwd + "/"
    global Fundamental_URL
    Fundamental_URL = ("https://www.macrotrends.net/stocks/charts/")

def grab_OHLC(ticker):
    """Grabs OHLC data from Yahoo Finance and return it as a dataframe """

    fyf.pdr_override()
    global Historical_Prices
    Historical_Prices = pdr.get_data_yahoo(ticker, start, end, inplace=False)
    #st.write(Historical_Prices)
    return Historical_Prices

def grab_historical_EPS(ticker):
    """Scrapes earnings from ycharts and return it as a dataframe' """
    df = pd.read_html(Fundamental_URL+ticker+"/"+ticker+"/eps-earnings-per-share-diluted")[1]
    all_earnings = pd.DataFrame(data = df, columns=None)
    all_earnings.columns = ['Date','EPS']
    all_earnings['Date'] = pd.to_datetime(all_earnings['Date'])
    all_earnings['EPS'] = all_earnings['EPS'].str.replace('$', '', regex=True).astype(float) # omits '$', please update if not working in future
    all_earnings.set_index('Date', inplace = True) # make date column the index
    all_earnings = all_earnings.sort_index() #make sure data is stored oldest at top, newest on bottom
    
    return all_earnings

def edit_EPS(ticker,Earnings_df):
    """Read in Earning_df and create new column EPS_ttm and return updated Earning_df """
    Earnings_df['EPS_ttm'] = Earnings_df['EPS'].rolling(window=4,center=False).sum()
    return Earnings_df

def merge_OHLC_EPS_ttm(ticker,OHLC_df,Earning_df):
    """Merge Historical_Prices and Earnings_df and return Merged_df """
    # frames = [OHLC_df,Earning_df] #list of the dataframes that are loaded

    #loop that assigns eps to proper trade dates
    for eps_day in Earning_df.index:
        # print(eps_day)
        for trade_day in OHLC_df.index:
            #print(trade_day)
            if eps_day <= trade_day:
                OHLC_df.at[trade_day,'EPS_ttm'] = Earning_df.loc[eps_day]['EPS_ttm']
                #print(ohlc_data.at[trade_day,'EPS'])
    OHLC_df.dropna(inplace=True)
    return OHLC_df

def calc_PE_ratio(ticker,Merged_df):
    """Read in Merged_df and create a new column 'PE_ttm_Ratio' then return updated Merged_df """
    Merged_df['PE_ttm_Ratio'] = (Merged_df['Adj Close'] / Merged_df['EPS_ttm'])
    #st.write(Merged_df)
    return Merged_df

def calc_volatility(ticker, OHLC_full_df):
    """Reads and edits the Original OHLC_full_df to calculate Adj Close_LogRet and Volatility then return updated OHLC_full_df """
    # create new column 'Adj Close_LogRet'
    OHLC_full_df['Adj Close_LogRet'] = np.log(OHLC_full_df['Adj Close'] / OHLC_full_df['Adj Close'].shift(1))
    OHLC_full_df['Volatility'] = OHLC_full_df['Adj Close_LogRet'].rolling(window=30,center=False).std() * np.sqrt(252)
    # st.write(OHLC_full_df)
    return OHLC_full_df

def get_PE_stats(ticker,Merged_df):
    """Read in Merged_df and get PE stats returned by a dictionary """
    PE_stats = {}
    PE_stats["mean"] = Merged_df['PE_ttm_Ratio'].mean()
    PE_stats["std"] = Merged_df['PE_ttm_Ratio'].std()
    PE_stats["min"] = Merged_df['PE_ttm_Ratio'].min()
    PE_stats["max"] = Merged_df['PE_ttm_Ratio'].max()
    PE_stats["current"] = Merged_df['PE_ttm_Ratio'].iloc[-1]
    return PE_stats

def get_volume_stats(ticker,OHLC_full_df):
    """Read in original OHLC_full_df and get volume stats returned by a dictionary """
    volume_stats = {}
    volume_stats["mean"] = OHLC_full_df['Volume'].mean()
    volume_stats["std"] = OHLC_full_df['Volume'].std()
    volume_stats["min"] = OHLC_full_df['Volume'].min()
    volume_stats["max"] = OHLC_full_df['Volume'].max()
    volume_stats["current"] = OHLC_full_df['Volume'].iloc[-1]
    return volume_stats

def get_volatility_stats(ticker,OHLC_full_df):
    """Read in original OHLC_full_df and get volatility stats returned by a dictionary """
    volatility_stats = {}
    volatility_stats["mean"] = OHLC_full_df['Volatility'].mean()
    volatility_stats["std"] = OHLC_full_df['Volatility'].std()
    volatility_stats["min"] = OHLC_full_df['Volatility'].min()
    volatility_stats["max"] = OHLC_full_df['Volatility'].max()
    volatility_stats["current"] = OHLC_full_df['Volatility'].iloc[-1]
    return volatility_stats

def normal_distribution_curve(dict_stats, label):
    """Draws the normal distribution curve """
    ## Grab from the dictionary
    mean = dict_stats["mean"]
    std = dict_stats["std"]
    x = dict_stats["current"]
    
    # for simulating the data 
    increment = 0.01

    # If it is volume we need to change the increments
    if label.lower() == "volume":
        increment = 1000
    else:
        increment = 0.01

    # Creating the distribution
    # start from the lowest 
    start = math.floor(mean - (3 * std))
    stop = math.ceil(mean + (3 * std))
    data = np.arange(start, stop + 1, increment)
    pdf = norm.pdf(data, loc=mean, scale=std)               # loc is the mean, scale is the standard deviation

    # Visualizing the distribution
    ## Adjust figure size for better viewing
    plt.figure(figsize=(16, 8))
    
    ## Plot the graph 
    plt.plot(data, pdf, color='black')
    
    ### Shade the corresponding area
    plt.fill_between(data, pdf, 0, where=(data <= x), color='#f59592')
    plt.fill_between(data, pdf, 0, where=(data > x), color='#97f4a6')
    #plt.axvline(x, color = '#383838')
    
    ## Correct labels
    plt.title('Probability Curve for {}'.format(ticker),fontsize=20)
    plt.xlabel(str(label))
    plt.ylabel('Probability Density')
    #plt.show()
    st.pyplot(plt)

def get_CDF(dict_stats):
    """Grabs the CDF of one of the corresponding measurements (PE, Volume, Volatility) """
    mean = dict_stats["mean"]
    std = dict_stats["std"]
    current = dict_stats["current"]

    probability = round(norm.cdf(current, mean, std),4)
    return probability

def suggestion(CDF,measure):
    """Gives suggestion based on its cdf and measure (PE,Volume,Volatility) """
    if measure == "PE":
        if CDF > .50:
            st.markdown('We suggest to **SELL** if within your risk.')
        elif CDF == .50:
            st.markdown('We suggest to **HOLD**.')
        else:
            st.markdown('We suggest to **BUY** if within your risk.')

    elif measure == "Volatility":
        if CDF > .50:
            st.markdown('**Sell Call** or **Buy Put** if within your risk')
        elif CDF == .50:
            st.markdown('We suggest to **HOLD**.')
        else:
            st.markdown('**Buy Call** or **Sell Put** if within your risk ')

    elif measure == "Volume":
        if CDF > .5:
            st.markdown('**Breakout** or **Breakdown**')
        elif CDF == .5:
            st.markdown('We suggest to **HOLD**.')
        else:
            st.markdown('**Capitulation Period**')

    else:
        st.error("NO MEASSURE SELECTED")

if __name__ == '__main__':
    main()
