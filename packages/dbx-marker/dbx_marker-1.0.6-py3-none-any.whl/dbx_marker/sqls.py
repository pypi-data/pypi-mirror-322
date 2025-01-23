INITIALIZE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS delta.`{delta_table_path}` (
    pipeline_name STRING,
    marker_type STRING,
    value STRING,
    updated_at TIMESTAMP
)
USING DELTA
"""

GET_MARKER_SQL = """
SELECT value, marker_type
FROM delta.`{delta_table_path}`
WHERE pipeline_name = '{pipeline_name}'
ORDER BY updated_at DESC
LIMIT 1
"""

UPDATE_MARKER_SQL = """
MERGE INTO delta.`{delta_table_path}` AS target
USING (
    SELECT '{pipeline_name}' AS pipeline_name, 
           '{value}' AS value,
           '{marker_type}' AS marker_type,
           '{now}' AS updated_at
) AS source
ON target.pipeline_name = source.pipeline_name
WHEN MATCHED THEN
    UPDATE SET target.value = source.value, target.marker_type = source.marker_type, target.updated_at = source.updated_at
WHEN NOT MATCHED THEN
    INSERT (pipeline_name, value, marker_type, updated_at)
    VALUES (source.pipeline_name, source.value, source.marker_type, source.updated_at)
"""

DELETE_MARKER_SQL = """
DELETE FROM delta.`{delta_table_path}`
WHERE pipeline_name = '{pipeline_name}'
"""
