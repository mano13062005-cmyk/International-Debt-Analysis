"""International Debt Analysis — beginner-friendly Streamlit dashboard."""
import pandas as pd
import plotly.express as px
import mysql.connector
import streamlit as st

st.set_page_config(page_title='International Debt Analysis', page_icon='🌍', layout='wide')
st.title('🌍 International Debt Analysis Dashboard')
st.caption('World Bank International Debt Statistics • debt stock measures in current US dollars')

@st.cache_data(ttl=300)
def load_data():
    connection = mysql.connector.connect(**dict(st.secrets['mysql']))
    try:
        query = '''SELECT c.country_name, d.country_code, i.series_name, d.series_code,
                          d.year, d.debt_value
                   FROM debt_data d
                   JOIN countries c ON c.country_code=d.country_code
                   JOIN indicators i ON i.series_code=d.series_code'''
        return pd.read_sql(query, connection)
    finally:
        connection.close()

try:
    df = load_data()
except Exception as exc:
    st.error('Could not load MySQL data. Check your secrets.toml, schema.sql and import_data.py.')
    st.code(str(exc))
    st.stop()
if df.empty:
    st.warning('No records found. Run: python import_data.py')
    st.stop()

# DT.DOD.DECT.CD is the total external debt stock indicator; other components
# overlap and must NOT be summed to estimate global debt.
TOTAL = 'DT.DOD.DECT.CD'
options = df[['series_code','series_name']].drop_duplicates().sort_values('series_name')
labels = dict(zip(options.series_code, options.series_name))
if TOTAL not in labels:
    st.error('Total external debt stocks indicator is missing from this dataset.')
    st.stop()

with st.sidebar:
    st.header('Filters')
    indicator = st.selectbox('Debt indicator', options.series_code.tolist(),
        index=options.series_code.tolist().index(TOTAL), format_func=lambda c: labels[c])
    subset = df[df.series_code == indicator]
    years = sorted(subset.year.unique().tolist())
    selected_year = st.selectbox('Year', years, index=len(years)-1)
    countries = sorted(subset.country_name.unique().tolist())
    selected_countries = st.multiselect('Countries for trend comparison', countries,
        default=[c for c in ['India','China','Brazil'] if c in countries])

current = subset[subset.year == selected_year].copy()
# Exclude regional aggregates when using global rankings where possible. The CSV
# has country codes and may also contain aggregates; keep only three-letter codes
# but some aggregates also have 3 letters, so labels are not automatically inferred.
current = current.sort_values('debt_value', ascending=False)
st.info('Values represent debt stocks, not annual new borrowing. Different debt indicators can overlap; do not add them together. Some dataset entries may represent aggregates.')

col1, col2, col3 = st.columns(3)
col1.metric('Countries / entries', f'{current.country_code.nunique():,}')
col2.metric('Indicators available', f'{df.series_code.nunique():,}')
col3.metric('Selected year', str(selected_year))

st.subheader('Top 10 country/area entries')
top = current.head(10).sort_values('debt_value')
fig = px.bar(top, x='debt_value', y='country_name', orientation='h',
    labels={'debt_value':'Debt stock (current US$)', 'country_name':'Country / area'},
    title=f'{labels[indicator]} — {selected_year}')
st.plotly_chart(fig, use_container_width=True)

st.subheader('Year-wise debt trend')
if selected_countries:
    trend = subset[subset.country_name.isin(selected_countries)]
    fig2 = px.line(trend, x='year', y='debt_value', color='country_name', markers=True,
        labels={'year':'Year','debt_value':'Debt stock (current US$)','country_name':'Country'})
    st.plotly_chart(fig2, use_container_width=True)
else:
    st.info('Choose countries in the sidebar to view trends.')

st.subheader('Country comparison')
compare = current[current.country_name.isin(selected_countries)]
if not compare.empty:
    st.plotly_chart(px.bar(compare, x='country_name', y='debt_value',
        labels={'country_name':'Country','debt_value':'Debt stock (current US$)'}), use_container_width=True)

st.subheader('Data table and download')
search = st.text_input('Search country name')
view = current[current.country_name.str.contains(search, case=False, na=False)] if search else current
st.dataframe(view[['country_name','year','series_name','debt_value']], use_container_width=True, hide_index=True)
st.download_button('Download filtered CSV', view.to_csv(index=False).encode('utf-8'),
                   'debt_analysis_filtered.csv', 'text/csv')
st.caption('Tip: use SQL_queries.sql in MySQL Workbench to practice SQL analysis.')
