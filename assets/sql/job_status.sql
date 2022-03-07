SELECT
    j.job_name
,   j.ts
,   j.status
,   j.error_message
,   j.skip_reason
FROM testdb.ketl.job_status_snapshot AS j
ORDER BY
    j.ts DESC
