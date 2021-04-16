SELECT t.*
FROM (
    SELECT DISTINCT ON (crc.table_name)
        crc.ts AT TIME ZONE 'America/Los_Angeles' AS ts
    ,   crc.table_name
    ,   crc.variance_ct
    ,   (crc.variance_pct * 100)::FLOAT AS variance_pct
    ,   crc.missing_id_ct
    ,   crc.missing_id_examples
    ,   crc.extra_id_ct
    ,   crc.extra_id_examples
    FROM aud.carelogic_row_comparison crc
    WHERE
        ABS(variance_pct) >= 0.01
        AND NOT EXISTS (
            SELECT 1
            FROM aud.carelogic_row_comparison AS c2
            WHERE
                crc.table_name = c2.table_name
                AND ABS(variance_pct) < 0.01
                AND c2.ts > crc.ts
        )
    ORDER BY crc.table_name, crc.ts DESC
) AS t
ORDER BY
    t.ts DESC
;
