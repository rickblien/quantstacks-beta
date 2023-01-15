import streamlit as st

st.title('DISCOUNTED CASH FLOW VALUATION (DCF)')

st.header('Discount Rate (WACC)')

st.write('COST OF EQUITY')

# RISK FREE RATE
st.write('Risk Free Rate')
def risk_free_rate(country_option):
    try:
        # Scrape Counties 10 years bond rate
        import pandas as pd
        countries_10_years_bond_rate = pd.read_html("http://www.worldgovernmentbonds.com/", header=0)[1]
        countries_10_years_bond_rate

        # Filter out Selected country 10 years bond

        # Calculate: Selected Country Default Spread = Selected Country 10 years bond - USA 10 years bond

        # Calculate: Selected Country Risk Free Rate = USA 10 years bond - Selected Country Default Spread

    except:
        pass 

st.write('Beta')

st.write('Equity Risk Premium')
# Selected Country Risk Premium

# Selected Equity Risk Premium


st.write('COST OF DEBT')

st.write('Average Yield on Debt')

st.write('Tax Shield')


st.header('Terminal Value')

st.header('Projected Cash Flow')