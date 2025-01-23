CREATE OR REPLACE FUNCTION create_table_from_json(definition JSONB, reset BOOLEAN DEFAULT FALSE)
RETURNS VOID AS $$
local spi = require("pllua.spi")

local function execute_sql(sql)
    local status, result = pcall(function()
        return spi.execute(sql)
    end)
    if not status then
        error("Failed to execute SQL: " .. tostring(result))
    end
    return result
end

local nullval = {}  -- use some unique object to mark nulls
local def = definition{ null = nullval, pg_numeric = true }
local table_name = def.table_name
local table_fields = def.table_fields
local fts_fields = def.fts_fields or {}

local columns = {}
local existing_columns = {}
local has_id_primary_key = false
local index_columns = {}

if reset then
    local drop_table_sql = string.format("DROP TABLE IF EXISTS %s CASCADE;", table_name)
    execute_sql(drop_table_sql)
end


for key, value in pairs(table_fields) do
    if key:lower() == "id" then
        -- Ensure 'id' is always PRIMARY KEY
        table.insert(columns, key .. " " .. value .. " PRIMARY KEY")
        has_id_primary_key = true
    else
        table.insert(columns, key .. " " .. value)
        if key:lower() ~= "data" then
            table.insert(index_columns, key)
        end        
    end
    existing_columns[key:lower()] = true
end

print("INdex columns " .. tostring(index_columns))

-- Add necessary columns only if they don't exist
local required_columns = {
    {name = "name", type = "TEXT NOT NULL"},
    {name = "creation_date", type = "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"},
    {name = "mod_date", type = "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"},
    {name = "data", type = "JSONB"}
}

for _, col in ipairs(required_columns) do
    if not existing_columns[col.name:lower()] then
        table.insert(columns, col.name .. " " .. col.type)
        table.insert(index_columns, col.name)
    end
end

-- If 'id' wasn't provided, add it as PRIMARY KEY
if not has_id_primary_key then
    table.insert(columns, 1, "id TEXT PRIMARY KEY")
end

-- Join columns with commas
local columns_string = table.concat(columns, ", ")

-- Construct the CREATE TABLE statement
local create_table_sql = string.format("CREATE TABLE IF NOT EXISTS %s (%s);", table_name, columns_string)

-- Conditionally construct the DROP TABLE statement

-- Execute the CREATE TABLE statement
execute_sql(create_table_sql)

-- Create an index for each column
for _, column in ipairs(index_columns) do
    local index_sql = string.format("CREATE INDEX IF NOT EXISTS idx_%s_%s ON %s (%s);", 
                                    table_name, column, table_name, column)
    execute_sql(index_sql)
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
    execute_sql(fts_table_sql)
end

return
$$ LANGUAGE pllua;