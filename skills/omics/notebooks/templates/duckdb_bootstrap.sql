-- DuckDB bootstrap example
-- Keep SQL readable with CTEs and explicit names.

-- Example: create a table from a TSV file (path supplied in Python)
-- CREATE OR REPLACE TABLE events AS
-- SELECT * FROM read_csv_auto('.../data/raw/events.tsv', delim='\t');

-- Example query pattern
WITH
events_daily AS (
  SELECT
    CAST(event_time AS DATE) AS day,
    COUNT(*) AS n_events
  FROM events
  GROUP BY 1
)
SELECT *
FROM events_daily
ORDER BY day;
