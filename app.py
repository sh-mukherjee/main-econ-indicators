import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from dbnomics import fetch_series, fetch_series_by_api_link

@st.cache_data
def fetch_clean_combine():
    dfcli = fetch_series('OECD', 'MEI_CLI', 'LOLITOAA...M', max_nb_series=55).query("value != 'NA'").query("period >= '2020'")
    dfbci = fetch_series('OECD', 'MEI_CLI', 'BSCICP03...M', max_nb_series=55).query("value != 'NA'").query("period >= '2020'")
    dfcci = fetch_series('OECD', 'MEI_CLI', 'CSCICP03...M', max_nb_series=55).query("value != 'NA'").query("period >= '2020'")

    dfcli['Indicator'] = 'CLI'
    dfbci['Indicator'] = 'BCI'
    dfcci['Indicator'] = 'CCI'

    # Combine the data into one dataframe
    df = pd.concat([dfcli, dfbci, dfcci], ignore_index=True)
    return df

st.title('OECD Main Economic Indicators')
st.write("""In this dashboard we will look at trends in three main economic indicators published by the OECD -- composite leading indicator, business confidence index and consumer confidence index. These data series can be downloaded directly from the [OECD Stats Website](https://stats.oecd.org/Index.aspx?DatasetCode=MEI_CLI), but here we will look at a very easy way to obtain the data from the year 2020 onwards using DBnomics.

[DBnomics](https://db.nomics.world/) is "One website aggregating global data and one API. Data series delivered in various formats (CSV, Excel XLSX, JSON). Direct access from your statistical software (R and Python)."
       """)
col1, col2, col3 = st.columns(3)

with col1:
    with st.expander("Composite Leading Indicator (CLI)"):
        st.write("""
        The composite leading indicator (CLI) is designed to provide early signals of turning points in business cycles showing fluctuation of the economic activity around its long term potential level. CLIs show short-term economic movements in qualitative rather than quantitative terms.
    
        CITATION: OECD (2021), Composite leading indicator (CLI) (indicator). doi: 10.1787/4a174487-en
        """)

with col2:
    with st.expander("Business Confidence Index (BCI)"):
        st.write("""
        This business confidence indicator provides information on future developments, based upon opinion surveys on developments in production, orders and stocks of finished goods in the industry sector. It can be used to monitor output growth and to anticipate turning points in economic activity. Numbers above 100 suggest an increased confidence in near future business performance, and numbers below 100 indicate pessimism towards future performance.
    
        CITATION: OECD (2021), Business confidence index (BCI) (indicator). doi: 10.1787/3092dc4f-en
        """)

with col3:
    with st.expander("Consumer Confidence Index (CCI)"):
        st.write("""
        This consumer confidence indicator provides an indication of future developments of households' consumption and saving, based upon answers regarding their expected financial situation, their sentiment about the general economic situation, unemployment and capability of savings. An indicator above 100 signals a boost in the consumers' confidence towards the future economic situation, as a consequence of which they are less prone to save, and more inclined to spend money on major purchases in the next 12 months. Values below 100 indicate a pessimistic attitude towards future developments in the economy, possibly resulting in a tendency to save more and consume less.
    
        CITATION: OECD (2021), Consumer confidence index (CCI) (indicator). doi: 10.1787/46434d78-en
        """)

# Creating the Streamlit app
df = fetch_clean_combine()

locations = df.Country.unique() # list of regions or countries

#dropdown selection widget for countries and regions, multiple selections allowed
Regions = st.multiselect('Choose the countries or regions',locations, default = ['United States'])

# Create enhanced figure with better formatting
fig = px.line(df[df.Country.isin(Regions)],
              x='period',
              y='value',
              color='Country',
              color_discrete_sequence=px.colors.qualitative.Set2,
              facet_row='Indicator',
              template='plotly_white',
              labels={'period': 'Date', 'value': 'Index Value'},
              height=800
            )

# Update layout for better appearance
fig.update_layout(
    font=dict(size=12),
    hovermode='x unified',
    showlegend=True,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    )
)

# Update axes
fig.update_xaxes(
    showgrid=True,
    gridwidth=1,
    gridcolor='lightgray',
    title_font=dict(size=13, color='#333'),
    tickfont=dict(size=11)
)

fig.update_yaxes(
    showgrid=True,
    gridwidth=1,
    gridcolor='lightgray',
    title_font=dict(size=13, color='#333'),
    tickfont=dict(size=11)
)

# Make lines slightly thicker and add markers
fig.update_traces(
    line=dict(width=2.5),
    marker=dict(size=4),
    mode='lines+markers'
)

# Add reference line at 100 for BCI and CCI (confidence threshold)
for i, indicator in enumerate(['CLI', 'BCI', 'CCI']):
    if indicator in ['BCI', 'CCI']:
        fig.add_hline(
            y=100, 
            line_dash="dash", 
            line_color="gray", 
            opacity=0.5,
            row=i+1,
            annotation_text="Confidence Threshold (100)",
            annotation_position="right"
        )

st.plotly_chart(fig, use_container_width=True)