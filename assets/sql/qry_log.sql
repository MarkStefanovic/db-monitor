SELECT
    a.query_start
,   a.usename AS user
,   a.query
,   age(now()
,   a.query_start) AS "age"
,   a.pid
FROM pg_stat_activity AS a
WHERE
    a.query IS NOT NULL
    AND TRIM(a.query) NOT IN ('', 'COMMIT', 'ROLLBACK', 'SHOW TRANSACTION ISOLATION LEVEL')
    AND a.query NOT LIKE 'DEALLOCATE %'
    AND a.query NOT LIKE 'autovacuum: %'
    AND a.query <> 'set client_encoding to ''WIN1252'''
    AND a.query NOT LIKE 'BEGIN;SELECT ts AT TIME ZONE ''America/%'
    AND a.query NOT LIKE 'BEGIN;SELECT blocked_locks.pid AS blocked_pid%'
    AND a.query NOT LIKE 'BEGIN;SELECT a.query_start%'
ORDER BY a.query_start DESC;