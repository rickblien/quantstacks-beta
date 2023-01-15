import streamlit as st
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

# Import required libraries pages 7
import yfinance as yf
import pandas as pd
from bokeh.plotting import figure
import bokeh.models as bmo
from bokeh.palettes import Paired11
from bokeh.io import show
from bokeh.models import ColumnDataSource, HoverTool
import math

# list all rows
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

st.set_page_config(
    page_title="QuantStacks beta",
    page_icon="👋",
)

st.write("# QuantStacks beta! 👋")

st.sidebar.success("Select a demo above.")
