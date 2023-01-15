import streamlit as st
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

# list all rows
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

st.set_page_config(
    page_title="QuantStacks beta",
    page_icon="👋",
)

st.write("# QuantStacks beta! 👋")

st.sidebar.success("Select a demo above.")
