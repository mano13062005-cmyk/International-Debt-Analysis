USE international_debt;
-- Training exercises. Totals across years or overlapping indicators are NOT meaningful global debt totals.
-- Some country codes represent aggregates; filter them before interpreting global rankings.

-- Query 1
SELECT DISTINCT country_name FROM countries ORDER BY country_name;

-- Query 2
SELECT COUNT(*) AS countries FROM countries;

-- Query 3
SELECT COUNT(*) AS indicators FROM indicators;

-- Query 4
SELECT * FROM debt_data LIMIT 10;

-- Query 5
SELECT year, SUM(debt_value) AS total FROM debt_data WHERE series_code='DT.DOD.DECT.CD' GROUP BY year ORDER BY year DESC;

-- Query 6
SELECT series_name FROM indicators ORDER BY series_name;

-- Query 7
SELECT country_code, COUNT(*) AS records FROM debt_data GROUP BY country_code ORDER BY records DESC;

-- Query 8
SELECT * FROM debt_data WHERE series_code='DT.DOD.DECT.CD' AND debt_value > 1000000000 LIMIT 100;

-- Query 9
SELECT MIN(debt_value), MAX(debt_value), AVG(debt_value) FROM debt_data WHERE series_code='DT.DOD.DECT.CD';

-- Query 10
SELECT COUNT(*) AS records FROM debt_data;

-- Query 11
SELECT country_code, SUM(debt_value) AS total FROM debt_data WHERE series_code='DT.DOD.DECT.CD' GROUP BY country_code ORDER BY total DESC;

-- Query 12
SELECT c.country_name,d.debt_value FROM debt_data d JOIN countries c USING(country_code) WHERE d.series_code='DT.DOD.DECT.CD' AND d.year=(SELECT MAX(year) FROM debt_data WHERE series_code='DT.DOD.DECT.CD') ORDER BY d.debt_value DESC LIMIT 10;

-- Query 13
SELECT country_code, AVG(debt_value) AS avg_debt FROM debt_data WHERE series_code='DT.DOD.DECT.CD' GROUP BY country_code;

-- Query 14
SELECT series_code, SUM(debt_value) AS total FROM debt_data GROUP BY series_code ORDER BY total DESC;

-- Query 15
SELECT series_code, SUM(debt_value) AS total FROM debt_data GROUP BY series_code ORDER BY total DESC LIMIT 1;

-- Query 16
SELECT country_code, debt_value FROM debt_data WHERE series_code='DT.DOD.DECT.CD' ORDER BY debt_value ASC LIMIT 1;

-- Query 17
SELECT country_code,series_code,SUM(debt_value) AS total FROM debt_data GROUP BY country_code,series_code;

-- Query 18
SELECT country_code,COUNT(DISTINCT series_code) AS indicators FROM debt_data GROUP BY country_code;

-- Query 19
SELECT country_code,SUM(debt_value) AS total FROM debt_data WHERE series_code='DT.DOD.DECT.CD' GROUP BY country_code HAVING total > (SELECT AVG(debt_value) FROM debt_data WHERE series_code='DT.DOD.DECT.CD');

-- Query 20
SELECT country_code, SUM(debt_value) AS total, DENSE_RANK() OVER(ORDER BY SUM(debt_value) DESC) AS debt_rank FROM debt_data WHERE series_code='DT.DOD.DECT.CD' GROUP BY country_code;

-- Query 21
SELECT series_code,SUM(debt_value) AS total FROM debt_data GROUP BY series_code ORDER BY total DESC LIMIT 5;

-- Query 22
SELECT country_code,year,ROUND(100*debt_value/SUM(debt_value) OVER(PARTITION BY year),2) AS pct FROM debt_data WHERE series_code='DT.DOD.DECT.CD';

-- Query 23
SELECT * FROM (SELECT country_code,series_code,year,debt_value,ROW_NUMBER() OVER(PARTITION BY series_code,year ORDER BY debt_value DESC) AS rn FROM debt_data) x WHERE rn<=3 AND year=2020;

-- Query 24
SELECT country_code,MAX(debt_value)-MIN(debt_value) AS range_value FROM debt_data WHERE series_code='DT.DOD.DECT.CD' GROUP BY country_code;

-- Query 25
CREATE OR REPLACE VIEW top_10_debt AS SELECT c.country_name,d.debt_value,d.year FROM debt_data d JOIN countries c USING(country_code) WHERE d.series_code='DT.DOD.DECT.CD' AND d.year=2020 ORDER BY d.debt_value DESC LIMIT 10;

-- Query 26
SELECT country_code,year,debt_value,CASE WHEN debt_value>=100000000000 THEN 'High' WHEN debt_value>=10000000000 THEN 'Medium' ELSE 'Low' END AS category FROM debt_data WHERE series_code='DT.DOD.DECT.CD';

-- Query 27
SELECT country_code,year,debt_value,SUM(debt_value) OVER(PARTITION BY country_code ORDER BY year) AS cumulative FROM debt_data WHERE series_code='DT.DOD.DECT.CD';

-- Query 28
SELECT series_code,AVG(debt_value) AS average FROM debt_data GROUP BY series_code HAVING average>(SELECT AVG(debt_value) FROM debt_data);

-- Query 29
SELECT country_code,year,debt_value FROM debt_data WHERE series_code='DT.DOD.DECT.CD' AND debt_value>0.05*(SELECT SUM(x.debt_value) FROM debt_data x WHERE x.series_code='DT.DOD.DECT.CD' AND x.year=debt_data.year);

-- Query 30
SELECT country_code,series_code,total FROM (SELECT country_code,series_code,SUM(debt_value) AS total,ROW_NUMBER() OVER(PARTITION BY country_code ORDER BY SUM(debt_value) DESC) AS rn FROM debt_data GROUP BY country_code,series_code) x WHERE rn=1;
