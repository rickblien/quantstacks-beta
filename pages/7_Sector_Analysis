## Import required libraries
import yfinance as yf
import pandas as pd
from bokeh.plotting import figure
import bokeh.models as bmo
from bokeh.palettes import Paired11
from bokeh.io import show
from bokeh.models import ColumnDataSource, HoverTool
import math

# Input definition
depth = 'sub_sector'
filter = 'Health Care'

# Main body
index_name = 'SP_500'
companies = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies', flavor='bs4')[0]
code_label = 'Symbol'
company_label = 'Security'

companies_codes = companies[code_label].to_list()

df_all = pd.DataFrame()
color_df = pd.DataFrame({0})

for stock in companies_codes:

    try:
        stock_data = yf.Ticker(stock.replace(".",""))
        stock_name = companies[company_label].loc[companies[code_label] == stock].values[0]
        df_all[stock_name] = stock_data.history(start="2017-01-01")['Close']

        color_df[stock_name] = 'blue'

    except:
        pass

color_df = color_df.drop(columns=[0])

df_all = df_all.loc[df_all.index > '2019' ,:]

df_ytd = df_all.loc[df_all.index > '2020' ,:]
df_hist = df_all.loc[df_all.index < '2020' ,:]

df_ytd_pc = (df_ytd.iloc[-1, :] - df_ytd.iloc[0, :]) / df_ytd.iloc[0, :] * 100

df_hist_pc = df_hist.pct_change()*100
std_stocks = df_hist_pc.std()

col_names = ['Name', 'YTD_performance', 'Typical_volatility', 'Sector', 'SubSector']
df_summary = pd.DataFrame(columns=col_names)

for stock in std_stocks.index.values:

    name = stock
    pc_change = df_ytd_pc[companies['Security'].loc[companies['Security'] == stock]].values[0]
    volatility = std_stocks[companies['Security'].loc[companies['Security'] == stock]].values[0]
    sector = companies['GICS Sector'].loc[companies['Security'] == stock].values[0]
    sub_sector = companies['GICS Sub-Industry'].loc[companies['Security'] == stock].values[0]

    new_row = pd.DataFrame([[name, pc_change, volatility, sector, sub_sector]], columns=col_names)
    df_summary = df_summary.append(new_row)


source = ColumnDataSource(data=dict(cum_sum_ytd=df_summary.YTD_performance, std=df_summary.Typical_volatility,
                                    sector=df_summary.Sector, sub_sector=df_summary.SubSector, name=df_summary.Name,
                                    ))

# PLOTS 

if depth == 'sector':

    df_sector = df_summary.groupby(['Sector']).mean()
    df_sector = df_sector.sort_values(by=['YTD_performance'], ascending=False)

    source2 = ColumnDataSource(data=dict(cum_sum_ytd=df_sector.YTD_performance.to_list(), sector=df_sector.index.to_list()))

    p = figure(plot_height=700, plot_width=1200, x_range=df_sector.index.to_list(), toolbar_location='right', y_range=[-50, 50],
               title='Year-to-date performance of individual sectors (S&P 500 stocks)', tools="save")

    color_map = bmo.CategoricalColorMapper(factors=df_summary['Sector'].unique(), palette=Paired11)

    p.vbar(x='sector', top='cum_sum_ytd', width=0.9, source=source2, fill_color={'field': 'sector', 'transform': color_map},
            legend_label='sector', line_width=0)

    p.xaxis.major_label_orientation = math.pi/3
    p.yaxis.axis_label = 'Year to date average performance (%)'

    p.title.text_font_size = '12pt'
    p.yaxis.axis_label_text_font_size = '12pt'

    show(p)


elif depth == 'sub_sector':

    df_sub_sector_pre = df_summary.loc[df_summary['Sector'] == filter]
    df_sub_sector_pre = df_sub_sector_pre.groupby(['SubSector']).mean()
    df_sub_sector_pre = df_sub_sector_pre.sort_values(by=['YTD_performance'], ascending=False)

    if len(df_sub_sector_pre) > 11:
        sliced_df = df_sub_sector_pre.head(5)
        df_sub_sector = sliced_df.append(df_sub_sector_pre.tail(6))
    else:
        df_sub_sector = df_sub_sector_pre

    source3 = ColumnDataSource(data=dict(cum_sum_ytd=df_sub_sector.YTD_performance.to_list(), sector=df_sub_sector.index.to_list()))

    color_map = bmo.CategoricalColorMapper(factors=df_sub_sector.index.unique(), palette=Paired11)

    p = figure(plot_height=700, plot_width=1200, x_range=df_sub_sector.index.to_list(), toolbar_location='right', tools="save",
               title='Year-to-date performance of individual sub-sectors (S&P 500 stocks). Sector: ' + filter,
               y_range=[min(df_sub_sector.YTD_performance.to_list()) - 10, max(df_sub_sector.YTD_performance.to_list()) + 10])

    p.vbar(x='sector', top='cum_sum_ytd', width=0.9, source=source3, fill_color={'field': 'sector', 'transform': color_map},
            legend_label='sector', line_width=0)

    p.xaxis.major_label_orientation = math.pi/3
    p.yaxis.axis_label = 'Year to date average performance (%)'

    p.title.text_font_size = '12pt'
    p.yaxis.axis_label_text_font_size = '12pt'
    p.legend.location = 'top_right'

    show(p)