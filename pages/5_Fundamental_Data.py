import streamlit as st
from datetime import datetime
import datetime as dt
import pandas_datareader.data as reader
import lxml
from lxml import html
import requests
import numpy as np
import pandas as pd
import yfinance as yf
import yahoo_fin.stock_info as si


# s&p 500 tickers
sp500_tickers = si.tickers_sp500()
sp500_tickers.insert(0, 'Spy')
sp500_tickers.insert(1, 'All')

selected_option = st.multiselect(
    label='What are your favorite stocks',
    options=sp500_tickers,
    default=["TSLA"],)

if "All" in selected_option:
    selected_option = sp500_tickers[1:]


for ticker in selected_option:
    quote = si.get_quote_table(ticker)     
    st.write(ticker)


    # yahoo get page
    def get_page(url):
        # Set up the request headers that we're going to use, to simulate
        # a request by the Chrome browser. Simulating a request from a browser
        # is generally good practice when building a scraper
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'close',
            'DNT': '1', # Do Not Track Request Header 
            'Pragma': 'no-cache',
            'Referrer': 'https://google.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
        }

        return requests.get(url, headers=headers)

    # yahoo parse rows
    def parse_rows(table_rows):
        parsed_rows = []

        for table_row in table_rows:
            parsed_row = []
            el = table_row.xpath("./div")

            none_count = 0

            for rs in el:
                try:
                    (text,) = rs.xpath('.//span/text()[1]')
                    parsed_row.append(text)
                except ValueError:
                    parsed_row.append(np.NaN)
                    none_count += 1

            if (none_count < 4):
                parsed_rows.append(parsed_row)
                
        return pd.DataFrame(parsed_rows)

    # yahoo clean data
    def clean_data(df):
        df = df.set_index(0) # Set the index to the first column: 'Period Ending'.
        df = df.transpose() # Transpose the DataFrame, so that our header contains the account names
        
        # Rename the "Breakdown" column to "Date"
        cols = list(df.columns)
        cols[0] = 'Date'
        df = df.set_axis(cols, axis='columns', inplace=False)
        
        numeric_columns = list(df.columns)[1::] # Take all columns, except the first (which is the 'Date' column)

        for column_index in range(1, len(df.columns)): # Take all columns, except the first (which is the 'Date' column)
            df.iloc[:,column_index] = df.iloc[:,column_index].str.replace(',', '') # Remove the thousands separator
            df.iloc[:,column_index] = df.iloc[:,column_index].astype(np.float64) # Convert the column to float64
            
        return df

    # yahoo scrape table
    def scrape_table(url):
        # Fetch the page that we're going to parse
        page = get_page(url);

        # Parse the page with LXML, so that we can start doing some XPATH queries
        # to extract the data that we want
        tree = html.fromstring(page.content)

        # Fetch all div elements which have class 'D(tbr)'
        table_rows = tree.xpath("//div[contains(@class, 'D(tbr)')]")
        
        # Ensure that some table rows are found; if none are found, then it's possible
        # that Yahoo Finance has changed their page layout, or have detected
        # that you're scraping the page.
        assert len(table_rows) > 0
        
        df = parse_rows(table_rows)
        df = clean_data(df)
            
        return df

    # # Get yahoo Balance Sheet
    balance_sheet = scrape_table('https://finance.yahoo.com/quote/' + ticker + '/balance-sheet?p=' + ticker)
    st.write(ticker + ' Balance Sheet')
    balance_sheet

    # # Get yahoo Income Statement
    income_statement = scrape_table('https://finance.yahoo.com/quote/' + ticker + '/financials?p=' + ticker)
    st.write(ticker + ' Income Statement')
    income_statement

    # # Get yahoo Cash Flow
    cash_flow = scrape_table('https://finance.yahoo.com/quote/' + ticker + '/cash-flow?p=' + ticker)
    st.write(ticker + ' Cash Flow Statement')
    cash_flow

    

