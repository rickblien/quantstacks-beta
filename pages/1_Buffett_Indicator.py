import streamlit as st
import yahoo_fin.stock_info as si
import pandas as pd

header = st.container()

with header:
    st.title("Warren Buffett Valuation")

    # get tickers
    sp500_tickers = si.tickers_sp500()
    sp500_tickers.insert(0, 'ALL')

    # MultiSelection ticker bar
    selected_option = st.multiselect(
        label='What are your favorite stocks',
        options=sp500_tickers,
        default=["TSLA"],
        )
    
    if "All" in selected_option:
        selected_option = sp500_tickers[1:]

    for stock in selected_option:
        quote = si.get_quote_table(stock)    
        st.write(stock)

        # get Beta
        st.write('Beta')
        beta = float(quote['Beta (5Y Monthly)'])
        st.write(beta)

        # get Market Cap
        st.write('Market Cap')
        mc = str(quote['Market Cap'])
        if mc[-1] == 'T':
            fmc = float(mc.replace('T',''))
            marketCap = fmc*1000000000000
            st.write(marketCap)
        elif mc[-1] == 'B':
            fmc = float(mc.replace('B',''))
            marketCap = fmc*1000000000
            st.write(marketCap)
        elif mc[-1] == 'M':
            fmc = float(mc.replace('M',''))
            marketCap = fmc*1000000
            st.write(marketCap)  