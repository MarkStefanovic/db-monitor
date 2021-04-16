SELECT req.*
FROM (
    SELECT ts AT TIME ZONE 'America/Los_Angeles' AS ts, 'MED' AS src, username, report AS request
    FROM med.report_request
    WHERE username <> 'marks'

    UNION ALL

    SELECT ts AT TIME ZONE 'America/Los_Angeles' AS ts, 'MGT' AS src, username, report AS request
    FROM mgt.report_request
    WHERE username <> 'marks'

    UNION ALL

    SELECT ur.ts AT TIME ZONE 'America/Los_Angeles' AS ts, 'RPT' AS src, ur.username, ur.request
    FROM rpt.user_request ur
    WHERE ur.username <> 'marks'
) AS req
ORDER BY req.ts DESC
LIMIT 20