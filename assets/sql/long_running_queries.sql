SELECT
    pid
,   NOW() - pg_stat_activity.query_start AS duration
,   query
,   state
FROM pg_stat_activity
WHERE
    (NOW() - pg_stat_activity.query_start) > INTERVAL '15 minutes';