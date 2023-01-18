import streamlit as st
import yfinance as yf
import yahoo_fin.stock_info as si
import pandas as pd
import numpy as np
import requests
import lxml
from lxml import html
import warnings
warnings.filterwarnings('ignore')

dcf = st.container()

with dcf:
    st.title("Discount Cash Flow")

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

    for symbol in selected_option:
        quote = si.get_quote_table(symbol)     
        st.write(symbol)
        ticker = symbol

        # Get Risk Free Rate
        countries_10_years_bond_rate = pd.read_html("http://www.worldgovernmentbonds.com/", header=0)[1]

        if symbol.endswith(('.SS', '.SZ')):
            # China 10 years bond
            filter_china_10y_bond = (countries_10_years_bond_rate['Unnamed: 1'] == 'China')
            china_10years_bond = countries_10_years_bond_rate[filter_china_10y_bond]
            china_10years_bond = china_10years_bond.iloc[0]['10Y Bond'] 
            china_10years_bond = float(china_10years_bond.replace("%","")) /100
            # st.write("china_10years_bond = {}".format(china_10years_bond))

            # China Default Spread
            filter_china_default_spread = (countries_10_years_bond_rate['Unnamed: 1'] == 'China')
            china_default_spread = countries_10_years_bond_rate[filter_china_default_spread]
            china_default_spread = china_default_spread.iloc[0]['Spread vs.1']
            china_default_spread = float(china_default_spread.replace("bp","")) /10000
            # print("china_default_spread = {}".format(china_default_spread)) 

            # China Risk Free Rate
            risk_free_rate = china_10years_bond - china_default_spread
            # st.write("risk_free_rate = {}".format(risk_free_rate))
            st.write("China's Risk Free Rate")
            st.write(risk_free_rate)

        else:
            # USA 10 years bond
            filter_usa_10years_bond = (countries_10_years_bond_rate['Unnamed: 1'] == 'United States')
            usa_10years_bond = countries_10_years_bond_rate[filter_usa_10years_bond]
            usa_10years_bond = usa_10years_bond.iloc[0]['10Y Bond'] 
            usa_10years_bond = float(usa_10years_bond.replace("%","")) /100
            # print("usa_10years_bond = {}".format(usa_10years_bond))

            # USA Risk Free Rate
            risk_free_rate = usa_10years_bond
            # print("risk_free_rate = {}".format(risk_free_rate))
            st.write("USA's Risk Free Rate")
            st.write(risk_free_rate)

        # get Beta
        try:
            st.text('Beta')
            beta = float(quote['Beta (5Y Monthly)'])
            st.write(beta)
        except:
            pass

        
        # get Market Cap
        try:
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
        except:
            pass

        # Get Fundamental Data
        try:
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
            pd.set_option('display.max_colwidth', None)
            pd.set_option('expand_frame_repr', False)

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
            
            # get balance sheet
            try:
                df_balance_sheet = scrape_table('https://finance.yahoo.com/quote/' + symbol + '/balance-sheet?p=' + symbol)
                df_balance_sheet = df_balance_sheet.set_index('Date')
                st.write(symbol + ' Balance Sheet')
                df_balance_sheet
            except:
                st.write(symbol + ' balance sheet failed')
                pass 
            
            # get income statement
            try:
                df_income_statement = scrape_table('https://finance.yahoo.com/quote/' + symbol + '/financials?p=' + symbol)
                df_income_statement = df_income_statement.set_index('Date')
                st.write(symbol + ' Income Statement')
                df_income_statement
            except:
                st.write(symbol + ' income statement failed')
                pass 

            # get cash flow statement
            try:
                df_cash_flow = scrape_table('https://finance.yahoo.com/quote/' + symbol + '/cash-flow?p=' + symbol)
                df_cash_flow = df_cash_flow.set_index('Date')
                st.write(symbol + ' Cash Flow Statement')
                df_cash_flow
            except:
                st.write(symbol + ' cash flow statement failed')
                pass
            
            # Get Total Debt
            try:
                Total_Debt = df_balance_sheet['Total Debt'][0]
                st.write(symbol + ' Total Debt')
                st.write(Total_Debt)
            except:
                st.write(symbol + ' Total Debt Failed!')
                pass
            
            # Calculate Weight of Equity
            try:
                Weight_of_Equity = marketCap / (marketCap + Total_Debt)
                st.write(symbol + ' Weight of Equity')
                st.write(Weight_of_Equity)
            except:
                st.write(symbol + ' Weight of Equity Failed!')
                pass 
        
            # Calculate Weight of Debt
            try:
                Weight_of_Debt = Total_Debt / (marketCap + Total_Debt)
                st.write(symbol + ' Weight of Debt')
                st.write(Weight_of_Debt)                
            except:
                st.write(symbol + ' Weight of Debt Failed!')
                pass

            # Get Interest Expense  
            try:
                Interest_Expenses = df_income_statement['Interest Expense'][0]
                st.write(symbol + ' Interest Expense')
                st.write(Interest_Expenses)
            except:
                st.write(symbol + ' Interest Expense Failed!')
                pass

            # Get Income Tax Expense
            try:
                Income_Tax_Expense = df_income_statement['Tax Provision'][0]
                st.write(symbol + ' Income_Tax_Expense')
                st.write(Income_Tax_Expense)                
            except:
                st.write(symbol + ' Income Tax Expense Failed!')
                pass 

            # Get Income Before Tax
            try:
                Income_Before_Tax = df_income_statement['Pretax Income'][0]
                st.write(symbol + ' Income_Before_Tax')
                st.write(Income_Before_Tax)                
            except:
                st.write(symbol + ' Income_Before_Tax Failed')
                pass 

            # Calculate effective tax rate
            try:
                Effective_Tax_Rate = Income_Tax_Expense / Income_Before_Tax
                st.write(symbol + ' Effective Tax Rate')
                st.write(Effective_Tax_Rate)
            except:
                st.write(symbol + ' Effective Tax Rate Failed')
                pass
            
            # Interest Coverage Ratio (Estimating Synthetic Ratings) = EBIT / Interest Expenses


            # Discount Rate (WACC)
            # try:
            #     Discount_Rate_WACC = (Weight_of_Equity * Cost_of_Equity) + (Weight_of_Debt * Cost_of_Debt) * (1 - Effective_Tax_Rate)
            # except:
            #     pass 

            # Analyst Growth Estimate
            try:
                symbol = symbol.upper()
                analysts = si.get_analysts_info(symbol)
                analysts_growth_estimate = analysts['Growth Estimates'][symbol][5]
                analysts_growth_estimate = float(analysts_growth_estimate.replace("%","")) /100
                st.write(symbol + ' Analysts Growth Estimate')
                st.write(analysts_growth_estimate)
            except:
                st.write(symbol + ' Analysts Growth Estimate Failed')
                pass

            # Symbol current price
            try:
                current_price = si.get_live_price(symbol)
                st.write(symbol + ' Current Price')
                st.write(current_price)
            except:
                st.write(symbol + ' current price failed')
                pass

            # ttm cash flow
            try:
                ttm_cashflow = current_price * risk_free_rate
                st.write(symbol + ' ttm cashflow')
                st.write(ttm_cashflow)
            except:
                st.write(symbol + ' ttm cashflow failed')
                pass

            # projected cashflow
            try:
                years = [1,2,3,4,5]
                futurefreecashflow = []
                for year in years:
                    cashflow = ttm_cashflow * (1 + analysts_growth_estimate)**year
                    futurefreecashflow.append(cashflow)
                st.write(symbol + ' projected cashflow statement')
                st.write(futurefreecashflow)
            except:
                st.write(symbol + ' projected cashflow failed')
                pass

            # Expected Return on symbol
            try:
                from scipy import optimize

                def fun(r):
                    r1 = 1 + r
                    return futurefreecashflow[0]/r1 +  futurefreecashflow[1]/r1**2 + futurefreecashflow[2]/r1**3 + futurefreecashflow[3]/r1**4 + futurefreecashflow[4]/r1**5 * (1 + (1+risk_free_rate)/(r-risk_free_rate)) - current_price

                roots = optimize.root(fun, [.1])
                expected_return_on_stock = float(roots.x)
                st.write(symbol + ' Expected Return on Stock')
                st.write(expected_return_on_stock)
            except:
                st.write(symbol + ' Expected Return on Stock failed')
                pass
            
            # Implied Equity Risk Premium
            try:
                implied_equity_risk_premium = expected_return_on_stock - risk_free_rate
                st.write(symbol + ' Implied Equity Risk Premium')
                st.write(implied_equity_risk_premium)
            except:
                st.write(symbol + ' implied equity rick premium failed')
                pass 

            # Discounted Future Cash Flow
            # try:
            #     discountedfuturefreecashflow = []
            #     for i in range(0, len(years)):
            #         discountedfuturefreecashflow.append(futurefreecashflow[i]/discountfactor[i])
            #     discountedfuturefreecashflow
            # except:
            #     pass 


        except:
            pass   