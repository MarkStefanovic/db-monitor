SELECT
    ts AT TIME ZONE 'America/Los_Angeles' AS ts
,   sp_name
,   message
FROM etl.sp_log sl ORDER BY ts DESC
LIMIT 100;