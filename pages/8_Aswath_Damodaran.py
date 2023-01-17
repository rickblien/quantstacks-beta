import streamlit as st

header = st.container()

with header:
    st.title('Aswath Damodaran Valuation')
    st.text('Professor of Finance at the Stern School of Business at New York University')

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(["Risk Free Rate", "Equity Risk Premium", "Betas", "Cost of Debt", "Cost of Equity", "Estimating Cash Flows", "Estimating Growth", "Terminal Value"])

with tab1:
    st.header('Risk Free Rate')
    # Risk Free Rate Video   
    risk_free_rate_url = ('https://www.youtube.com/watch?v=xV80dt1OZtQ&list=PLUkh9m2BorqnKWu0g5ZUps_CbQ-JGtbI9&index=3') 
    # Checkbox to show Risk Free Rate Video
    if st.checkbox('Show Risk Free Rate Video'):
        st.video(risk_free_rate_url)

    # # Scrape Countries 10 years government bond rates
    # import pandas as pd
    # countries_10_years_bond_rate = pd.read_html("http://www.worldgovernmentbonds.com/", header=0)[1]
    # countries_10_years_bond_rate.rename(columns={"Unnamed: 0":"Nan","Unnamed: 1":"country_name","Rating":"rating","10Y Bond":"10y_bond","10Y Bond.1":"10y_bond_1","Bank":"bank", "Spread vs":"spread_vs", "Spread vs.1":"spread_vs_1"},inplace=True)
    # country_name = countries_10_years_bond_rate['country_name'][1:].tolist()
    # # country_name.insert(0, 'All')

    # country_option = st.selectbox(
    #     label='Which country?',
    #     options=country_name,)

    # # if "All" in country_option:
    # #     country_option = country_name[1:]

    def risk_free_rate(country_option):
        try:
            # st.header(country_option)
            # Filter out selected country 10 years bond
            filter_country_10y_bond = (countries_10_years_bond_rate['country_name'] == country_option)
            country_10years_bond = countries_10_years_bond_rate[filter_country_10y_bond]
            country_10years_bond = country_10years_bond.iloc[0]['10y_bond'] 
            country_10years_bond = float(country_10years_bond.replace("%","")) /100
            # st.write('10 Years Bond')
            # st.write(country_10years_bond)

            # Calculate Default Spread
            # st.header('Default Spread')
            # st.write("Country Default Spread = Country 10 Years Bond - USA 10 Years Bond")
            
            # USA 10 years bond
            filter_usa_10years_bond = (countries_10_years_bond_rate['country_name'] == 'United States')
            usa_10years_bond = countries_10_years_bond_rate[filter_usa_10years_bond]
            usa_10years_bond = usa_10years_bond.iloc[0]['10y_bond'] 
            usa_10years_bond = float(usa_10years_bond.replace("%","")) /100
            # st.write('USA 10 years bond')
            # st.write(usa_10years_bond)

            # Selected Country Default Spread
            country_default_spread_usd = country_10years_bond - usa_10years_bond
            # st.write('Country Default Spread')
            # st.write(country_default_spread_usd)
            # st.write("Country Default Spread = Country 10 Years Bond - USA 10 Years Bond")

            # Calculate Selected Country Risk Free Rate
            country_risk_free_rate = usa_10years_bond - country_default_spread_usd
            # st.write("Risk Free Rate")
            # st.write(country_risk_free_rate)
            # st.write("Country Risk Free Rate = USA 10 Years Bond - Country Default Spread")

            listd = [country_10years_bond, usa_10years_bond,country_default_spread_usd,country_risk_free_rate]
            return listd

        except:
            st.write(country_option + "failed!")
            pass

    # Scrape Countries 10 years government bond rates
    import pandas as pd
    countries_10_years_bond_rate = pd.read_html("http://www.worldgovernmentbonds.com/", header=0)[1]
    countries_10_years_bond_rate.rename(columns={"Unnamed: 0":"Nan","Unnamed: 1":"country_name","Rating":"rating","10Y Bond":"10y_bond","10Y Bond.1":"10y_bond_1","Bank":"bank", "Spread vs":"spread_vs", "Spread vs.1":"spread_vs_1"},inplace=True)
    country_name = countries_10_years_bond_rate['country_name'][1:].tolist()   

    country_name.insert(0, 'All')

    country_option = st.multiselect(
        label='Which country?',
        options=country_name,
        default=['United States'],
        )

    if "All" in country_option:
        country_option = country_name[1:]

    country_data_in_table = []
    temp_table = []

    for country in country_option:
        temp_table = risk_free_rate(country)
        temp_table.insert(0,country)
        country_data_in_table.append(temp_table)

    colu = ["Country", "10years bond", "USA 10years bond","Default Spread", "Risk Free Rate"]
    inde = range(len(country_option))
    df2 = pd.DataFrame(data= country_data_in_table,index=inde,columns=colu)

    with st.expander(" Risk Free Rate", expanded=True):
        st.table(df2)
    
with tab2:
    st.header('Equity Risk Premium')
    # Equity Risk Premium Video   
    equity_risk_premium_url = ('https://www.youtube.com/watch?v=U3D9a_H_Vrs&list=PLUkh9m2BorqnKWu0g5ZUps_CbQ-JGtbI9&index=4') 
    
    # Checkbox to show Equity Risk Premium Video
    if st.checkbox('Show Equity Risk Premium Video'):
        st.video(equity_risk_premium_url)
    
    try:
        # Backward Looking Equity Risk Premiums
        ## Calculate USA index average returns
        import yfinance as yf
        import numpy as np
        import pandas as pd
        ticker = '^GSPC' # S&P 500
        data = yf.download(tickers=ticker, period='max', interval='1d')
        data['yearly_returns'] = data['Adj Close'].resample('Y').ffill().pct_change()
        data.dropna()
        usa_index_average_returns = data['yearly_returns'].mean()
        st.write('Backward Looking Equity Risk Premiums')
        st.write(usa_index_average_returns)    

        # Forward Looking Equity Risk Premiums
        ## Scrape S&P500 dividend & buyback data
        import pandas as pd
        import requests
        import urllib3
        urllib3.disable_warnings()
        import io
        url='https://pages.stern.nyu.edu/~adamodar/pc/datasets/histimpl.xls'
        requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL:@SECLEVEL=1'
        res = requests.get(url,verify=False)
        data = pd.read_excel(io.BytesIO(res.content),sheet_name='Historical Impl Premiums', header=6, nrows=62)
        data = data.dropna()

        # Scrape sp500 current price data
        import yahoo_fin.stock_info as si
        current_sp500_price = si.get_live_price("^GSPC")
        st.write('S&P 500 Current Price')
        st.write(current_sp500_price)

        # Calculate sp500 average yield return
        sp500_average_yield = data['Dividends + Buybacks'].mean() / current_sp500_price
        st.write('S&P 500 Average Yield Return')
        st.write(sp500_average_yield)

        # Calculate ttm sp500 cashflow
        ttm_sp500_cashflow = current_sp500_price * sp500_average_yield
        st.write('ttm S&P 500 Cashflow')
        st.write(ttm_sp500_cashflow)

        # Calculate sp500 analyst average growth estimate
        sp500_analyst_growth_estimate = data['Analyst Growth Estimate'].mean()
        st.write('S&P 500 Analyst Average Growth Estimate')
        st.write(sp500_analyst_growth_estimate)

        # Project sp500 future cashflow
        years = [1,2,3,4,5]
        futurefreecashflow = []
        for year in years:
            cashflow = ttm_sp500_cashflow*(1+sp500_analyst_growth_estimate)**year
            futurefreecashflow.append(cashflow)
        st.write('S&P 500 Future Cashflow')
        st.write(futurefreecashflow)

        # Calculate Expected Returns
        from scipy import optimize

        def fun(r):
            r1 = 1 + r
            return futurefreecashflow[0]/r1 +  futurefreecashflow[1]/r1**2 + futurefreecashflow[2]/r1**3 + futurefreecashflow[3]/r1**4 + futurefreecashflow[4]/r1**5 * (1 + (1+country_risk_free_rate)/(r-country_risk_free_rate)) - current_sp500_price

        roots = optimize.root(fun, [.1])
        expected_return_on_sp500 = float(roots.x)
        st.write('S&P 500 Expected Returns')
        st.write(expected_return_on_sp500)

        # Implied (forward looking) Equity Risk Premiums
        implied_equity_risk_premium = expected_return_on_sp500 - country_risk_free_rate
        st.write('Implied (forward looking) Equity Risk Premiums')
        st.write(implied_equity_risk_premium)

    except:
        pass

# with tab3:
#     st.header('Betas')
#     # Betas Video   
#     betas_url = ('https://www.youtube.com/watch?v=qKy5UGcvWaw&list=PLUkh9m2BorqnKWu0g5ZUps_CbQ-JGtbI9&index=5') 
#     # Checkbox to show Betas Video
#     if st.checkbox('Show Betas Video'):
#         st.video(betas_url)

#     # Beta
#     import yahoo_fin.stock_info as si
#     quote_table = si.get_quote_table(ticker)
#     st.write(quote_table)
#     # beta = quote_table['Beta (5Y Monthly)']
#     # st.write(beta)


# with tab4:
#     st.header('Cost of Debt')
#     # Cost of Debt and Capital Video   
#     cost_of_debt_and_capital_url = ('https://www.youtube.com/watch?v=N_FH89DCdGs&list=PLUkh9m2BorqnKWu0g5ZUps_CbQ-JGtbI9&index=6') 
#     # Checkbox to show Cost of Debt and Capital Video
#     if st.checkbox('Show Cost of Debt and Capital Video'):
#         st.video(cost_of_debt_and_capital_url)

# with tab5:
#     st.header('Cost of Equity')

# with tab6:
#     st.header('Estimating Cash Flows')
#     # Estimating Cash Flows Video   
#     estimating_cash_flows_url = ('https://www.youtube.com/watch?v=8gYT3Xgs6NE&list=PLUkh9m2BorqnKWu0g5ZUps_CbQ-JGtbI9&index=7') 
#     # Checkbox to show Estimating Cash Flows Video
#     if st.checkbox('Show Estimating Cash Flows Video'):
#         st.video(estimating_cash_flows_url)

#     # Cashflow projections
#     income_first_yr = 100
#     growth_rt = 0.06
#     discount_rt = 0.02

#     cashflow = [income_first_yr]
#     for i in range(29):
#         cashflow.append(cashflow[i] * (1 + growth_rt))

#     discount_vector = [discount_rt]
#     for i in range(29):
#         discount_vector.append(discount_vector[i] / (1 + discount_rt))

#     for i in zip(cashflow, discount_vector):
#         st.write(i)

#     discounted_cashflow = []
#     for item in zip(cashflow, discount_vector):
#         discounted_cashflow.append(item[0] * item[1])
        
#     st.table(discounted_cashflow)
    
#     import pandas as pd
#     df = pd.DataFrame({'Income':[100*1.06**i for i in range(30)],
#                     'Discount_vector':[1.02**(-i) for i in range(30)]})
#     st.table(df)

#     df['Discounted_cashflow'] = df['Income'] * df['Discount_vector']
#     st.table(df)      

# with tab7:
#     st.header('Estimating Growth')
#     # Estimating Growth Video   
#     estimating_growth_url = ('https://www.youtube.com/watch?v=fRNcP9xjk-8&list=PLUkh9m2BorqnKWu0g5ZUps_CbQ-JGtbI9&index=8') 
#     # Checkbox to show Estimating Growth Video
#     if st.checkbox('Show Estimating Growth Video'):
#         st.video(estimating_growth_url)

# with tab8:
#     st.header('Terminal Value')
#     # Terminal Value Video   
#     terminal_value_url = ('https://www.youtube.com/watch?v=83yR6EFEl5Y&list=PLUkh9m2BorqnKWu0g5ZUps_CbQ-JGtbI9&index=9') 
#     # Checkbox to show Terminal Value Video
#     if st.checkbox('Show Terminal Value Video'):
#         st.video(terminal_value_url)