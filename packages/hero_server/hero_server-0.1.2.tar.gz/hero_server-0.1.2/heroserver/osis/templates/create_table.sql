CREATE OR REPLACE FUNCTION create_table_from_json(
    definition JSONB,
    reset BOOLEAN DEFAULT FALSE
) RETURNS VOID AS $$
DECLARE
    table_name TEXT;
    table_fields JSONB;
    fts_fields TEXT[];
    columns TEXT := '';
    create_table_sql TEXT;
    drop_table_sql TEXT;
    fts_table_sql TEXT := '';
    field RECORD;
BEGIN
    -- Extract the values from the JSON object
    table_name := definition->>'table_name';
    table_fields := definition->'table_fields';
    fts_fields := ARRAY(SELECT jsonb_array_elements_text(definition->'fts_fields'));

    -- Iterate over the JSONB object to build the columns definition
    FOR field IN SELECT * FROM jsonb_each_text(table_fields)
    LOOP
        columns := columns || field.key || ' ' || field.value || ', ';
    END LOOP;

    -- Add the necessary columns
    columns := columns || 'id TEXT PRIMARY KEY, ';
    columns := columns || 'name TEXT NOT NULL, ';
    columns := columns || 'creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, ';
    columns := columns || 'mod_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, ';
    columns := columns || 'data JSON';

    -- Construct the CREATE TABLE statement
    create_table_sql := 'CREATE TABLE IF NOT EXISTS ' || table_name || ' (' || columns || ');';

    -- Conditionally construct the DROP TABLE statement
    IF reset THEN
        drop_table_sql := 'DROP TABLE IF EXISTS ' || table_name || ';';
        create_table_sql := drop_table_sql || create_table_sql;
    END IF;

    -- Add the FTS table and index if full-text search fields are provided
    IF array_length(fts_fields, 1) > 0 THEN
        fts_table_sql := 'CREATE TABLE IF NOT EXISTS ' || table_name || '_fts (' ||
                         'id TEXT PRIMARY KEY, ' ||
                         table_name || '_id TEXT REFERENCES ' || table_name || '(id), ' ||
                         'document tsvector);' ||
                         'CREATE INDEX IF NOT EXISTS idx_' || table_name || '_fts_document ' ||
                         'ON ' || table_name || '_fts USING GIN(document);';
        create_table_sql := create_table_sql || fts_table_sql;
    END IF;

    -- Execute the dynamic SQL
    EXECUTE create_table_sql;
END;
$$ LANGUAGE plpgsql;