CREATE DATABASE IF NOT EXISTS international_debt;
USE international_debt;
CREATE TABLE IF NOT EXISTS countries (
 country_code VARCHAR(12) PRIMARY KEY, country_name VARCHAR(150) NOT NULL
);
CREATE TABLE IF NOT EXISTS indicators (
 series_code VARCHAR(60) PRIMARY KEY, series_name VARCHAR(300) NOT NULL
);
CREATE TABLE IF NOT EXISTS debt_data (
 country_code VARCHAR(12) NOT NULL,
 series_code VARCHAR(60) NOT NULL,
 year SMALLINT NOT NULL,
 debt_value DOUBLE NOT NULL,
 PRIMARY KEY (country_code, series_code, year),
 FOREIGN KEY (country_code) REFERENCES countries(country_code),
 FOREIGN KEY (series_code) REFERENCES indicators(series_code),
 INDEX idx_year_series (year, series_code)
);
