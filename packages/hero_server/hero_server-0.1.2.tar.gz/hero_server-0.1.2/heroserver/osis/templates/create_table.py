CREATE OR REPLACE FUNCTION create_table_from_json(definition_json JSONB, reset BOOLEAN DEFAULT FALSE)
RETURNS VOID AS $$
import plpy
import json

def execute_sql(sql):
    try:
        plpy.execute(sql)
    except Exception as e:
        plpy.error(f"Failed to execute SQL: {str(e)}")

# Parse the JSONB input into a Python dictionary
definition = json.loads(definition_json)

table_name = definition['table_name']
table_fields = definition['table_fields']
fts_fields = definition.get('fts_fields', [])

columns = []
existing_columns = set()
has_id_primary_key = False
index_columns = []

if reset:
    drop_table_sql = f"DROP TABLE IF EXISTS {table_name} CASCADE;"
    execute_sql(drop_table_sql)

for key, value in table_fields.items():
    if key.lower() == "id":
        columns.append(f"{key} {value} PRIMARY KEY")
        has_id_primary_key = True
    else:
        columns.append(f"{key} {value}")
        if key.lower() != "data":
            index_columns.append(key)
    existing_columns.add(key.lower())

plpy.notice(f"Index columns {index_columns}")

required_columns = [
    {"name": "name", "type": "TEXT NOT NULL"},
    {"name": "creation_date", "type": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"},
    {"name": "mod_date", "type": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"},
    {"name": "data", "type": "JSONB"}
]

for col in required_columns:
    if col['name'].lower() not in existing_columns:
        columns.append(f"{col['name']} {col['type']}")
        index_columns.append(col['name'])

if not has_id_primary_key:
    columns.insert(0, "id TEXT PRIMARY KEY")

columns_string = ", ".join(columns)

create_table_sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_string});"
execute_sql(create_table_sql)

for column in index_columns:
    index_sql = f"CREATE INDEX IF NOT EXISTS idx_{table_name}_{column} ON {table_name} ({column});"
    execute_sql(index_sql)

if fts_fields:
    fts_table_sql = f"""
        CREATE TABLE IF NOT EXISTS {table_name}_fts (
            id TEXT PRIMARY KEY,
            {table_name}_id TEXT REFERENCES {table_name}(id),
            document tsvector
        );
        CREATE INDEX IF NOT EXISTS idx_{table_name}_fts_document ON {table_name}_fts USING GIN(document);
    """
    execute_sql(fts_table_sql)

$$ LANGUAGE plpython3u;