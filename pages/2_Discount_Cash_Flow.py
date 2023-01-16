import streamlit as st
import pandas as pd

# list all rows
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

st.title('DISCOUNTED CASH FLOW VALUATION (DCF)')


st.header('Discount Rate (WACC)')


st.write('COST OF EQUITY')

# RISK FREE RATE
st.write('Risk Free Rate')
def risk_free_rate(country_option):
    try:
        # Filter out selected country 10 years bond
        filter_country_10y_bond = (countries_10_years_bond_rate['country_name'] == country_option)
        country_10years_bond = countries_10_years_bond_rate[filter_country_10y_bond]
        country_10years_bond = country_10years_bond.iloc[0]['10y_bond'] 
        country_10years_bond = float(country_10years_bond.replace("%","")) /100

        # USA 10 years bond
        filter_usa_10years_bond = (countries_10_years_bond_rate['country_name'] == 'United States')
        usa_10years_bond = countries_10_years_bond_rate[filter_usa_10years_bond]
        usa_10years_bond = usa_10years_bond.iloc[0]['10y_bond'] 
        usa_10years_bond = float(usa_10years_bond.replace("%","")) /100

        # Calculate: Selected Country Default Spread
        country_default_spread_usd = country_10years_bond - usa_10years_bond

        # Calculate: Selected Country Risk Free Rate 
        country_risk_free_rate = usa_10years_bond - country_default_spread_usd
        
        # Create a list contains country_10years_bond, usa_10years_bond,country_default_spread_usd,country_risk_free_rate
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

# create an empty tables
country_data_in_table = []
temp_table = []

# streamlit multiselect dropdown bar
country_option = st.multiselect(
    label = "Which countries?",
    options = country_name,
    default = 'United States')

# loop through selected countries from multiselect dropdown bar
for country in country_option:
    temp_table = risk_free_rate(country)
    temp_table.insert(0,country)
    country_data_in_table.append(temp_table)

# Create a column nanmes for risk free rate table
risk_free_rate_column_names = ["Country", "10years bond", "USA 10years bond","Default Spread", "Risk Free Rate"]

# Create row length for risk free rate table
risk_free_rate_row_length = range(len(country_option))

# Create a DataFrame for risk free rate 
risk_free_rate_df = pd.DataFrame(data= country_data_in_table,index=risk_free_rate_row_length,columns=risk_free_rate_column_names)

# Display risk free rate DataFrame in Streamlit
st.table(risk_free_rate_df)


# BETA
st.write('Beta')

# IMPLIED EQUITY RISK PREMIUM
st.write('Implied Equity Risk Premium')

# Get current price of stock

# Get Risk Free Rate

# Scrape Analysts 5 years growth estimate

# Calculate Expected Return on Stock

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