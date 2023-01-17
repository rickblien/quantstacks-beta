import streamlit as st
import yfinance as yf 
import talib
import yahoo_fin.stock_info as si
import pandas as pd
from datetime import date
import matplotlib.pyplot as plt
import matplotlib.transforms as transforms

pd.set_option('display.max_colwidth', -1)
pd.set_option('expand_frame_repr', False)

header = st.container()
candlestick = st.container()


with header:
    st.title("Candlestick Patterns")

with candlestick:
    st.header('Stocks Fundamental Data')

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

    tab1, tab2, tab3, tab4 = st.tabs(["Reversals: Bull Market", "Continuations: Bull Market", "Reversals: Bear Market", "Continuations: Bear Market"])

    with tab1:
        st.header('Reversals: Bull Market')

        for stock in selected_option:
            df = yf.download(stock, period='max')
            st.write(stock)

            # Step 4: Adding trend resistance & support lines
            pivot_high_1=df['High'][-21:-1].max()
            pivot_high_2=df['High'][-55:-22].max()
            pivot_low_1=df['Low'][-21:-1].min()
            pivot_low_2=df['Low'][-55:-22].min()

            A=[df['High'][-21:-1].idxmax(), pivot_high_1]
            B=[df['High'][-55:-22].idxmax(), pivot_high_2]

            A1=[df['Low'][-21:-1].idxmin(), pivot_low_1]
            B1=[df['Low'][-55:-22].idxmin(), pivot_low_2]

            x1_high_values = [A[0], B[0]]
            y1_high_values = [A[1], B[1]]

            x1_low_values = [A1[0], B1[0]]
            y1_low_values = [A1[1], B1[1]]

            # Step 3: Visualization with Matplotlib
            plt.rcParams.update({'font.size': 10})
            fig, ax1 = plt.subplots(figsize=(14,7))

            ax1.set_ylabel('Price in €')
            ax1.set_xlabel('Date')
            ax1.set_title(stock)
            ax1.plot('Adj Close',data=df, label='Close Price', linewidth=0.5, color='blue')

            ax1.plot(x1_high_values, y1_high_values, color='g', linestyle='--', linewidth=0.5, label='Trend resistance')
            ax1.plot(x1_low_values, y1_low_values, color='r', linestyle='--', linewidth=0.5, label='Trend support')

            ax1.axhline(y=pivot_high_1, color='g', linewidth=6, label='First resistance line', alpha=0.2)
            ax1.axhline(y=pivot_low_1, color='r', linewidth=6, label='First support line', alpha=0.2)
            trans = transforms.blended_transform_factory(ax1.get_yticklabels()[0].get_transform(), ax1.transData)
            ax1.text(0,pivot_high_1, "{:.2f}".format(pivot_high_1), color="g", transform=trans,ha="right", va="center")
            ax1.text(0,pivot_low_1, "{:.2f}".format(pivot_low_1), color="r", transform=trans,ha="right", va="center")

            ax1.legend()
            ax1.grid()
            # plt.show()
            st.pyplot(plt)

            # Reversal Bull candlestick patterns
            reversals_bull_df = pd.DataFrame()
            reversals_bull_df['three_stars_in_the_south'] = talib.CDL3STARSINSOUTH(df['Open'], df['High'], df['Low'], df['Close'])
            
            three_stars_in_the_south_buy_days = reversals_bull_df[reversals_bull_df['three_stars_in_the_south'] ==100]
            three_stars_in_the_south_sell_days = reversals_bull_df[reversals_bull_df['three_stars_in_the_south'] ==-100]

            st.write('Buy Days')
            st.write(three_stars_in_the_south_buy_days.tail(3))

            st.write('Sell Days')
            st.write(three_stars_in_the_south_sell_days.tail(3))


            reversals_bull_df['three_line_strike'] = talib.CDL3LINESTRIKE(df['Open'], df['High'], df['Low'], df['Close'])

            three_line_strike_buy_days = reversals_bull_df[reversals_bull_df['three_line_strike'] ==100]
            three_line_strike_sell_days = reversals_bull_df[reversals_bull_df['three_line_strike'] ==-100]

            st.write('Buy Days')
            st.write(three_line_strike_buy_days.tail(3))

            st.write('Sell Days')
            st.write(three_line_strike_sell_days.tail(3))

            reversals_bull_df['three_white_soldiers'] = talib.CDL3WHITESOLDIERS(df['Open'], df['High'], df['Low'], df['Close'])
            
            three_white_soldiers_buy_days = reversals_bull_df[reversals_bull_df['three_white_soldiers'] ==100]
            three_white_soldiers_sell_days = reversals_bull_df[reversals_bull_df['three_white_soldiers'] ==-100]

            st.write('Buy Days')
            st.write(three_white_soldiers_buy_days.tail(3))

            st.write('Sell Days')
            st.write(three_white_soldiers_sell_days.tail(3))


            reversals_bull_df['engulfing'] = talib.CDLENGULFING(df['Open'], df['High'], df['Low'], df['Close'])

            engulfing_buy_days = reversals_bull_df[reversals_bull_df['engulfing'] ==100]
            engulfing_sell_days = reversals_bull_df[reversals_bull_df['engulfing'] ==-100]

            st.write('Buy Days')
            st.write(engulfing_buy_days.tail(3))

            st.write('Sell Days')
            st.write(engulfing_sell_days.tail(3))

            reversals_bull_df['morning_star'] = talib.CDLMORNINGSTAR(df['Open'], df['High'], df['Low'], df['Close'])


            morning_star_buy_days = reversals_bull_df[reversals_bull_df['morning_star'] ==100]
            morning_star_sell_days = reversals_bull_df[reversals_bull_df['morning_star'] ==-100]

            st.write('Buy Days')
            st.write(morning_star_buy_days.tail(3))

            st.write('Sell Days')
            st.write(morning_star_sell_days.tail(3))

            
    with tab2:
        st.header('Continuations: Bull Market') 

        for stock in selected_option:
            df = yf.download(stock, period='max')
            st.write(stock)

            # Step 4: Adding trend resistance & support lines
            pivot_high_1=df['High'][-21:-1].max()
            pivot_high_2=df['High'][-55:-22].max()
            pivot_low_1=df['Low'][-21:-1].min()
            pivot_low_2=df['Low'][-55:-22].min()

            A=[df['High'][-21:-1].idxmax(), pivot_high_1]
            B=[df['High'][-55:-22].idxmax(), pivot_high_2]

            A1=[df['Low'][-21:-1].idxmin(), pivot_low_1]
            B1=[df['Low'][-55:-22].idxmin(), pivot_low_2]

            x1_high_values = [A[0], B[0]]
            y1_high_values = [A[1], B[1]]

            x1_low_values = [A1[0], B1[0]]
            y1_low_values = [A1[1], B1[1]]

            # Step 3: Visualization with Matplotlib
            plt.rcParams.update({'font.size': 10})
            fig, ax1 = plt.subplots(figsize=(14,7))

            ax1.set_ylabel('Price in €')
            ax1.set_xlabel('Date')
            ax1.set_title(stock)
            ax1.plot('Adj Close',data=df, label='Close Price', linewidth=0.5, color='blue')

            ax1.plot(x1_high_values, y1_high_values, color='g', linestyle='--', linewidth=0.5, label='Trend resistance')
            ax1.plot(x1_low_values, y1_low_values, color='r', linestyle='--', linewidth=0.5, label='Trend support')

            ax1.axhline(y=pivot_high_1, color='g', linewidth=6, label='First resistance line', alpha=0.2)
            ax1.axhline(y=pivot_low_1, color='r', linewidth=6, label='First support line', alpha=0.2)
            trans = transforms.blended_transform_factory(ax1.get_yticklabels()[0].get_transform(), ax1.transData)
            ax1.text(0,pivot_high_1, "{:.2f}".format(pivot_high_1), color="g", transform=trans,ha="right", va="center")
            ax1.text(0,pivot_low_1, "{:.2f}".format(pivot_low_1), color="r", transform=trans,ha="right", va="center")

            ax1.legend()
            ax1.grid()
            # plt.show()
            st.pyplot(plt)

            # Continuations Bull candlestick patterns
            continuations_bull_df = pd.DataFrame()
            continuations_bull_df['mat_hold'] = talib.CDLMATHOLD(df['Open'], df['High'], df['Low'], df['Close'])
            continuations_bull_df['concealing_baby_swallow'] = talib.CDLCONCEALBABYSWALL(df['Open'], df['High'], df['Low'], df['Close'])
            continuations_bull_df['rising_three_methods'] = talib.CDLRISEFALL3METHODS(df['Open'], df['High'], df['Low'], df['Close'])
            continuations_bull_df['separating_lines'] = talib.CDLSEPARATINGLINES(df['Open'], df['High'], df['Low'], df['Close'])
            continuations_bull_df['doji_star'] = talib.CDLDOJISTAR(df['Open'], df['High'], df['Low'], df['Close'])
            continuations_bull_df.T
            st.write(continuations_bull_df.tail(3))

    with tab3:
        st.header('Reversals: Bear Market')

        for stock in selected_option:
            df = yf.download(stock, period='max')
            st.write(stock)

            # Step 4: Adding trend resistance & support lines
            pivot_high_1=df['High'][-21:-1].max()
            pivot_high_2=df['High'][-55:-22].max()
            pivot_low_1=df['Low'][-21:-1].min()
            pivot_low_2=df['Low'][-55:-22].min()

            A=[df['High'][-21:-1].idxmax(), pivot_high_1]
            B=[df['High'][-55:-22].idxmax(), pivot_high_2]

            A1=[df['Low'][-21:-1].idxmin(), pivot_low_1]
            B1=[df['Low'][-55:-22].idxmin(), pivot_low_2]

            x1_high_values = [A[0], B[0]]
            y1_high_values = [A[1], B[1]]

            x1_low_values = [A1[0], B1[0]]
            y1_low_values = [A1[1], B1[1]]

            # Step 3: Visualization with Matplotlib
            plt.rcParams.update({'font.size': 10})
            fig, ax1 = plt.subplots(figsize=(14,7))

            ax1.set_ylabel('Price in €')
            ax1.set_xlabel('Date')
            ax1.set_title(stock)
            ax1.plot('Adj Close',data=df, label='Close Price', linewidth=0.5, color='blue')

            ax1.plot(x1_high_values, y1_high_values, color='g', linestyle='--', linewidth=0.5, label='Trend resistance')
            ax1.plot(x1_low_values, y1_low_values, color='r', linestyle='--', linewidth=0.5, label='Trend support')

            ax1.axhline(y=pivot_high_1, color='g', linewidth=6, label='First resistance line', alpha=0.2)
            ax1.axhline(y=pivot_low_1, color='r', linewidth=6, label='First support line', alpha=0.2)
            trans = transforms.blended_transform_factory(ax1.get_yticklabels()[0].get_transform(), ax1.transData)
            ax1.text(0,pivot_high_1, "{:.2f}".format(pivot_high_1), color="g", transform=trans,ha="right", va="center")
            ax1.text(0,pivot_low_1, "{:.2f}".format(pivot_low_1), color="r", transform=trans,ha="right", va="center")

            ax1.legend()
            ax1.grid()
            # plt.show()
            st.pyplot(plt)

            # Reversals Bear candlestick patterns
            reversals_bear_df = pd.DataFrame()
            reversals_bear_df['three_star_in_the_south'] = talib.CDL3STARSINSOUTH(df['Open'], df['High'], df['Low'], df['Close'])
            reversals_bear_df['breakaway'] = talib.CDLBREAKAWAY(df['Open'], df['High'], df['Low'], df['Close'])
            reversals_bear_df['three_white_soldiers'] = talib.CDL3WHITESOLDIERS(df['Open'], df['High'], df['Low'], df['Close'])
            reversals_bear_df['three_line_strike'] = talib.CDL3LINESTRIKE(df['Open'], df['High'], df['Low'], df['Close'])
            reversals_bear_df['engulfing'] = talib.CDLENGULFING(df['Open'], df['High'], df['Low'], df['Close'])
            reversals_bear_df.T
            st.write(reversals_bear_df.tail(3))

    with tab4:
        st.header('Continuations: Bear Market')

        for stock in selected_option:
            df = yf.download(stock, period='max')
            st.write(stock)

            # Step 4: Adding trend resistance & support lines
            pivot_high_1=df['High'][-21:-1].max()
            pivot_high_2=df['High'][-55:-22].max()
            pivot_low_1=df['Low'][-21:-1].min()
            pivot_low_2=df['Low'][-55:-22].min()

            A=[df['High'][-21:-1].idxmax(), pivot_high_1]
            B=[df['High'][-55:-22].idxmax(), pivot_high_2]

            A1=[df['Low'][-21:-1].idxmin(), pivot_low_1]
            B1=[df['Low'][-55:-22].idxmin(), pivot_low_2]

            x1_high_values = [A[0], B[0]]
            y1_high_values = [A[1], B[1]]

            x1_low_values = [A1[0], B1[0]]
            y1_low_values = [A1[1], B1[1]]

            # Step 3: Visualization with Matplotlib
            plt.rcParams.update({'font.size': 10})
            fig, ax1 = plt.subplots(figsize=(14,7))

            ax1.set_ylabel('Price in €')
            ax1.set_xlabel('Date')
            ax1.set_title(stock)
            ax1.plot('Adj Close',data=df, label='Close Price', linewidth=0.5, color='blue')

            ax1.plot(x1_high_values, y1_high_values, color='g', linestyle='--', linewidth=0.5, label='Trend resistance')
            ax1.plot(x1_low_values, y1_low_values, color='r', linestyle='--', linewidth=0.5, label='Trend support')

            ax1.axhline(y=pivot_high_1, color='g', linewidth=6, label='First resistance line', alpha=0.2)
            ax1.axhline(y=pivot_low_1, color='r', linewidth=6, label='First support line', alpha=0.2)
            trans = transforms.blended_transform_factory(ax1.get_yticklabels()[0].get_transform(), ax1.transData)
            ax1.text(0,pivot_high_1, "{:.2f}".format(pivot_high_1), color="g", transform=trans,ha="right", va="center")
            ax1.text(0,pivot_low_1, "{:.2f}".format(pivot_low_1), color="r", transform=trans,ha="right", va="center")

            ax1.legend()
            ax1.grid()
            # plt.show()
            st.pyplot(plt)

            # Continuations Bear candlestick patterns
            continuations_bear_df = pd.DataFrame()
            continuations_bear_df['kicking'] = talib.CDLKICKING(df['Open'], df['High'], df['Low'], df['Close'])
            continuations_bear_df['rising_three_methods'] = talib.CDLRISEFALL3METHODS(df['Open'], df['High'], df['Low'], df['Close'])
            continuations_bear_df['separating_lines'] = talib.CDLSEPARATINGLINES(df['Open'], df['High'], df['Low'], df['Close'])
            continuations_bear_df['doji_star'] = talib.CDLDOJISTAR(df['Open'], df['High'], df['Low'], df['Close'])
            continuations_bear_df['hammer_inverted'] = talib.CDLINVERTEDHAMMER(df['Open'], df['High'], df['Low'], df['Close'])
            continuations_bear_df.T
            st.write(continuations_bear_df.tail(3))

