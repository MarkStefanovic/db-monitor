SELECT j.ts, j.job_name, j.execution_error_message
FROM etl.jobs j
WHERE j.execution_error_occurred = TRUE
ORDER BY ts DESC
LIMIT 50;
