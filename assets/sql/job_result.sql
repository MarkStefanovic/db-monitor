SELECT
    j.job_name
,   j.start_time
,   j.end_time
,   j.result
,   j.error_message
,   j.skip_reason
FROM ketl.job_result_snapshot AS j
ORDER BY
    j.end_time DESC
