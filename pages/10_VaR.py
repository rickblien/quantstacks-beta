import streamlit as st
import yfinance as yf
import yahoo_fin.stock_info as si
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')
import datetime as dt, matplotlib.pyplot as plt, scipy.stats as scs

st.title("VaR Monte Carlo Simulation")

# s&p 500 tickers
sp500_tickers = si.tickers_sp500()
sp500_tickers.insert(0, 'Spy')
sp500_tickers.insert(1, 'All')


selected_option = st.multiselect(
    label='What are your favorite stocks',
    options=sp500_tickers,
    default=["Spy"],
    )

if "All" in selected_option:
    selected_option = sp500_tickers[1:]

time = st.slider(
    'Select Duration of Trading Days',
    1, 756, (45))
st.write('time:', time)

n_sims = st.number_input('Number of Simulation',min_value=100000, max_value=100000000, step=100000)
st.write('Number of Simulation is: ', n_sims)


for stock in selected_option:
    df = yf.download(stock, period='max')
    st.write(stock)

# rename column names
df.rename(columns = {'Open':'open', 'High':'high', 'Low':'low','Close':'close','Adj Close':'adj_close','Volume':'volume'}, inplace = True)

df['returns'] = df.adj_close.pct_change()
df.dropna(inplace=True)

s0 = df.adj_close[-1] # current stock price

vol = df['returns'].std()*252**.5 # standard deviation or volatility

# n_sims = 1000000 # number of simulation
# Scrape Countries 10 years bond rate from website
import pandas as pd
countries_10_years_bond_rate = pd.read_html("http://www.worldgovernmentbonds.com/", header=0)[1]
# filter usa 10 years bond data
filter_usa_10years_bond = (countries_10_years_bond_rate['Unnamed: 1'] == 'United States')
usa_10years_bond = countries_10_years_bond_rate[filter_usa_10years_bond]
usa_10years_bond = usa_10years_bond.iloc[0]['10Y Bond'] 
usa_10years_bond = float(usa_10years_bond.replace("%","")) /100
rfr = usa_10years_bond

# rfr = 0 # risk free rate
# time = 45 # time period 45 days

d = (rfr * 0.5 * vol**2) * (time/252)
a = vol * np.sqrt(time/252)
r = np.random.normal(0,1,(n_sims,1)) # random number 0 to 1 for 1 million simulations

GBM_returns = s0 * np.exp(d + a*r) # Geometric Brownian Motion (GBM)

# pers = [0.01, 0.1, 1.0, 2.5, 5.0, 10.0] # confidence interval
confidence_interval = np.arange(0.01,0.11,0.01) # confidence interval

var = scs.scoreatpercentile(GBM_returns -1, confidence_interval)

df = pd.DataFrame(s0-var, confidence_interval, columns=['VaR'])
st.table(df)

plt.hist(GBM_returns, density=True, bins=100)
# plt.show()
st.pyplot(plt)

