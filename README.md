# International Debt Analysis — Python + MySQL + Streamlit

A beginner-friendly dashboard using the uploaded World Bank IDS CSV and the assignment requirements.

## Files
- `app.py`: Streamlit dashboard with Plotly charts, filters, search and CSV export.
- `import_data.py`: cleans CSV and imports debt stock observations to MySQL.
- `schema.sql`: normalized MySQL database tables with foreign keys.
- `SQL_queries.sql`: 30 SQL practice queries.
- `data/IDS_ALLCountries_Data.csv`: your original dataset.

## Setup on Windows (VS Code terminal)
1. Extract this ZIP. Open the extracted folder in VS Code.
2. Install Python dependencies: `python -m pip install -r requirements.txt`
3. Open MySQL Workbench and execute **all** of `schema.sql`.
4. Inside `.streamlit`, copy `secrets.toml.example` to `secrets.toml` and replace the placeholder password with your actual MySQL password. Never upload `secrets.toml` to GitHub.
5. In VS Code terminal run: `python import_data.py` (may take a few minutes).
6. Run: `python -m streamlit run app.py`.
7. Open the local URL printed in terminal, usually http://localhost:8501.
8. Open `SQL_queries.sql` in MySQL Workbench to explore 30 queries.

## Important interpretation notes
- Dashboard starts with `DT.DOD.DECT.CD`, total external debt stocks in current USD.
- Other debt stock indicators overlap; adding them produces double-counting.
- Adding values across years also does not give meaningful global debt stocks.
- The source may include regional/aggregate entities. Country comparisons must be interpreted carefully.
- The 30 SQL statements are learning exercises; some intentionally aggregate observations across years or components and should not be presented as economically meaningful global totals.
- Source data uses Latin-1 encoding; import script handles this.
- If you see an authentication error, check `.streamlit/secrets.toml` and verify MySQL Server is running.

## Data source
User-provided International Debt Statistics dataset (Jan 2022 assignment).
