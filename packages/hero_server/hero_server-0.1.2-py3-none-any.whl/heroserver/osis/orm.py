from typing import Dict, Type, List
import datetime
from dataclasses import dataclass, field
import psycopg2
from psycopg2.extras import Json

@dataclass
class ObjIndexDef:
    table_name: str
    table_fields: Dict[str, Type]
    fts_fields: List[str] = field(default_factory=list)  # full text fields

def sql_col_type(field_type: Type) -> str:
    if field_type == int:
        return "INTEGER"
    elif field_type == float:
        return "REAL"
    elif field_type == str:
        return "TEXT"
    elif field_type == bool:
        return "BOOLEAN"
    elif field_type == datetime.date:
        return "DATE"
    elif field_type == datetime.datetime:
        return "TIMESTAMP"
    else:
        return "TEXT"  # default type if none match

def obj_index_def_new(table_name: str, table_fields: Dict[str, Type], fts_fields: List[str]) -> ObjIndexDef:
    # Convert Python types to SQL types
    sql_table_fields = {field_name: sql_col_type(field_type) for field_name, field_type in table_fields.items()}
    
    # Create and return the ObjIndexDef instance
    return ObjIndexDef(
        table_name=table_name,
        table_fields=table_fields,
        fts_fields=fts_fields
    )

def sql_table_create(db, definition: ObjIndexDef, reset: bool = False) -> str:
    columns = []
    for field_name, field_type in definition.table_fields.items():
        if field_name not in ["id", "name", "creation_date", "mod_date", "data"]:
            sql_type = sql_col_type(field_type)
            columns.append(f"{field_name} {sql_type}")

    columns.append("id TEXT PRIMARY KEY")
    columns.append("name TEXT NOT NULL")
    columns.append("creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
    columns.append("mod_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
    columns.append("data JSON")

    columns_str = ", ".join(columns)

    create_table_sql = f"CREATE TABLE IF NOT EXISTS {definition.table_name} ({columns_str});"

    if reset:
        drop_table_sql = f"DROP TABLE IF EXISTS {definition.table_name};"
        create_table_sql = drop_table_sql + "\n" + create_table_sql

    if definition.fts_fields:
        fts_table_sql = f"""
        CREATE TABLE IF NOT EXISTS {definition.table_name}_fts (
            id TEXT PRIMARY KEY,
            {definition.table_name}_id TEXT REFERENCES {definition.table_name}(id),
            document tsvector
        );
        CREATE INDEX IF NOT EXISTS idx_{definition.table_name}_fts_document
        ON {definition.table_name}_fts USING GIN(document);
        """
        create_table_sql += "\n" + fts_table_sql
        
        c=db.db_connection()
        
        try:
            with c.cursor() as cursor:
                cursor.execute(create_table_sql)
            c.commit()  # Commit the transaction
            print("SQL script executed successfully.")
        except psycopg2.Error as e:
            c.rollback()  # Rollback on error
            print(f"An error occurred: {e}")    
    
    return create_table_sql

def insert_update(db, definition: ObjIndexDef, **args):
    table_name = definition.table_name
    fields = definition.table_fields.keys()
    c=db.db_connection()
    # Prepare the data
    data = {}
    for field in fields:
        if field in args:
            if isinstance(args[field], dict):
                data[field] = Json(args[field])
            else:
                data[field] = args[field]
        elif field not in ["id", "creation_date", "mod_date"]:
            data[field] = None

    # Ensure required fields are present
    if "id" not in data:
        raise ValueError("'id' field is required for insert/update operation")
    if "name" not in data:
        raise ValueError("'name' field is required for insert/update operation")

    # Set modification date
    data["mod_date"] = datetime.datetime.now()

    # Prepare SQL
    fields_str = ", ".join(data.keys())
    placeholders = ", ".join(["%s"] * len(data))
    update_str = ", ".join([f"{k} = EXCLUDED.{k}" for k in data.keys() if k != "id"])

    sql = f"""
    INSERT INTO {table_name} ({fields_str})
    VALUES ({placeholders})
    ON CONFLICT (id) DO UPDATE
    SET {update_str};
    """

    # Execute SQL
    try:
        with c.cursor() as cursor:
            cursor.execute(sql, list(data.values()))
        
        c.commit()
        
        # Update FTS table if necessary
        if definition.fts_fields:
            c.update_fts(definition, data)
        
        print(f"Successfully inserted/updated record with id {data['id']}")
    except psycopg2.Error as e:
        c.rollback()
        print(f"An error occurred: {e}")

def update_fts(db, definition: ObjIndexDef, data: dict):
    fts_table = f"{definition.table_name}_fts"
    fts_fields = definition.fts_fields
    c=db.db_connection()
    # Prepare FTS document
    fts_data = " ".join(str(data[field]) for field in fts_fields if field in data)
    
    sql = f"""
    INSERT INTO {fts_table} (id, {definition.table_name}_id, document)
    VALUES (%s, %s, to_tsvector(%s))
    ON CONFLICT (id) DO UPDATE
    SET document = to_tsvector(EXCLUDED.document);
    """
    
    try:
        with c.cursor() as cursor:
            cursor.execute(sql, (data['id'], data['id'], fts_data))
        c.commit()
        print(f"Successfully updated FTS for record with id {data['id']}")
    except psycopg2.Error as e:
        c.rollback()
        print(f"An error occurred while updating FTS: {e}")