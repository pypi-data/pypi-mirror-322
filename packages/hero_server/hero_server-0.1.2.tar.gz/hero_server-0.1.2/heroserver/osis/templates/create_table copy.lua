CREATE OR REPLACE FUNCTION create_table_from_json(definition JSONB, reset BOOLEAN DEFAULT FALSE)
RETURNS VOID AS $$
    local json = require("cjson")
    local def = json.decode(definition)
    local table_name = def.table_name
    local table_fields = def.table_fields
    local fts_fields = def.fts_fields or {}

    local columns = ""
    for key, value in pairs(table_fields) do
        columns = columns .. key .. " " .. value .. ", "
    end

    -- Add the necessary columns
    columns = columns .. "id TEXT PRIMARY KEY, "
    columns = columns .. "name TEXT NOT NULL, "
    columns = columns .. "creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, "
    columns = columns .. "mod_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, "
    columns = columns .. "data JSON"

    -- Construct the CREATE TABLE statement
    local create_table_sql = string.format("CREATE TABLE IF NOT EXISTS %s (%s);", table_name, columns)

    print("Create table " .. tostring(create_table_sql))

    -- Conditionally construct the DROP TABLE statement
    if reset then
        local drop_table_sql = string.format("DROP TABLE IF EXISTS %s;", table_name)
        create_table_sql = drop_table_sql .. create_table_sql
    end

    -- Add the FTS table and index if full-text search fields are provided
    if #fts_fields > 0 then
        local fts_table_sql = string.format([[
            CREATE TABLE IF NOT EXISTS %s_fts (
                id TEXT PRIMARY KEY,
                %s_id TEXT REFERENCES %s(id),
                document tsvector
            );
            CREATE INDEX IF NOT EXISTS idx_%s_fts_document ON %s_fts USING GIN(document);
        ]], table_name, table_name, table_name, table_name, table_name)
        create_table_sql = create_table_sql .. fts_table_sql
    end

    print("Create table fts" .. tostring(create_table_sql))

    -- Execute the dynamic SQL
    SPI.execute(create_table_sql)
$$ LANGUAGE pllua;