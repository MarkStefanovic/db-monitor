SELECT ts, batch, seconds, err, err_msg, running
FROM (
    SELECT DISTINCT ON (b.name)
        b.ts AT TIME ZONE 'America/Los_Angeles' AS ts
    ,   b.name AS batch
    ,   b.execution_millis / 1000 AS seconds
    ,   b.execution_error_occurred AS err
    ,   b.execution_error_message AS err_msg
    ,   b.running
    FROM etl.batches b
    ORDER BY
        b.name
    ,   b.ts DESC
    ) AS b
ORDER BY ts DESC;