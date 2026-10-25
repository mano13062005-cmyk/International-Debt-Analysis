"""Clean the uploaded CSV and load it into MySQL. Run after schema.sql."""
from pathlib import Path
import pandas as pd
import mysql.connector
import streamlit as st

BASE = Path(__file__).parent
SOURCE = BASE / 'data' / 'IDS_ALLCountries_Data.csv'
if not SOURCE.exists():
    raise SystemExit(f'Missing CSV file: {SOURCE}')

config = dict(st.secrets['mysql'])
connection = mysql.connector.connect(**config)
cursor = connection.cursor()

# Keep debt measures expressed in current US dollars. Percentage and year measures
# cannot be added together with dollar amounts.
raw = pd.read_csv(SOURCE, encoding='latin1', low_memory=False)
raw.columns = raw.columns.str.strip()
raw = raw.drop_duplicates(subset=['Country Code', 'Series Code'])
raw = raw[raw['Series Code'].astype(str).str.startswith('DT.DOD.') & raw['Series Code'].astype(str).str.endswith('.CD')].copy()
raw = raw.dropna(subset=['Country Code', 'Country Name', 'Series Code', 'Series Name'])
raw = raw[raw['Country Code'].astype(str).str.len() <= 12]
raw = raw[raw['Series Code'].astype(str).str.len() <= 60]
raw = raw[raw['Country Name'].astype(str).str.len() <= 150]
raw = raw[raw['Series Name'].astype(str).str.len() <= 300]
if raw.empty:
    raise SystemExit('No dollar-denominated debt stock indicators found in CSV.')

years = [c for c in raw.columns if str(c).isdigit() and len(str(c)) == 4]
long = raw.melt(id_vars=['Country Code', 'Series Code'], value_vars=years,
                var_name='year', value_name='debt_value')
long['debt_value'] = pd.to_numeric(long['debt_value'], errors='coerce')
long = long.dropna(subset=['debt_value'])
long['year'] = long['year'].astype(int)

countries = raw[['Country Code', 'Country Name']].drop_duplicates('Country Code')
indicators = raw[['Series Code', 'Series Name']].drop_duplicates('Series Code')
try:
    cursor.executemany('INSERT INTO countries VALUES (%s,%s) ON DUPLICATE KEY UPDATE country_name=VALUES(country_name)',
        [tuple(row) for row in countries.itertuples(index=False, name=None)])
    cursor.executemany('INSERT INTO indicators VALUES (%s,%s) ON DUPLICATE KEY UPDATE series_name=VALUES(series_name)',
        [tuple(row) for row in indicators.itertuples(index=False, name=None)])
    connection.commit()
    sql = '''INSERT INTO debt_data (country_code, series_code, year, debt_value)
             VALUES (%s,%s,%s,%s) ON DUPLICATE KEY UPDATE debt_value=VALUES(debt_value)'''
    records = [(str(a), str(b), int(c), float(d)) for a,b,c,d in long.itertuples(index=False, name=None)]
    for i in range(0, len(records), 2000):
        cursor.executemany(sql, records[i:i+2000])
        connection.commit()
        print(f'Imported {min(i+2000,len(records)):,} / {len(records):,} debt observations')
    print('SUCCESS: MySQL database is ready!')
finally:
    cursor.close()
    connection.close()
