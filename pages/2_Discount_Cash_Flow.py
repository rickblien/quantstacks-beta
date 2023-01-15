import streamlit as st

st.title('DISCOUNTED CASH FLOW VALUATION (DCF)')

st.header('Discount Rate (WACC)')

st.write('COST OF EQUITY')

# RISK FREE RATE
st.write('Risk Free Rate')
# def risk_free_rate(country_option):
#     try:
# Scrape Counties 10 years bond rate
import pandas as pd
countries_10_years_bond_rate = pd.read_html("http://www.worldgovernmentbonds.com/", header=0)[1]
st.write(countries_10_years_bond_rate)

# Rename column names
countries_10_years_bond_rate.rename(columns={"Unnamed: 0":"Nan","Unnamed: 1":"country_name","Rating":"rating","10Y Bond":"10y_bond","10Y Bond.1":"10y_bond_1","Bank":"bank", "Spread vs":"spread_vs_german", "Spread vs.1":"spread_vs_usa"},inplace=True)
st.write(countries_10_years_bond_rate)

# Get country name list
country_names_list = countries_10_years_bond_rate['country_name'].tolist()
st.write(country_names_list)

# Filter out Selected country 10 years bond

# Calculate: Selected Country Default Spread = Selected Country 10 years bond - USA 10 years bond

# Calculate: Selected Country Risk Free Rate = USA 10 years bond - Selected Country Default Spread

# except:
#     pass 

# BETA
st.write('Beta')

# IMPLIED EQUITY RISK PREMIUM
st.write('Implied Equity Risk Premium')
# Selected Country Risk Premium

# Selected Equity Risk Premium

# COST OF DEBT
st.write('COST OF DEBT')

# AVERAGE YIELD ON DEBT
st.write('Average Yield on Debt')

# TAX SHIELD
st.write('Tax Shield')





st.header('Terminal Value')

st.header('Projected Cash Flow')