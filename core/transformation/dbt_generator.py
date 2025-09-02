import os
import yaml
import json
import duckdb
from core.data_reader import read, input_path

db_path = "core/storage/duck_db"


def duckdb_client(database_name: str) -> None:
    if not os.path.exists(db_path):
        os.makedirs(db_path)
    db_file = os.path.join(db_path, f"{database_name}.duckdb")
    con = duckdb.connect(db_file)
    con.execute("CREATE SCHEMA IF NOT EXISTS public;")
    con.close()


# HELPER FUNCTIONS
def generate_sql_file(database, table, mapping, seeds_name):
    table_name = table['table_name']
    sql_lines = [
        f"-- Model for table: {table_name}",
        f"-- Source: seed '{seeds_name}.csv'",
        f"-- Database: {database}",
        "",
        f"SELECT"
    ]
    cols = []
     
    for col in table['columns']:
        inferred_col = col['name']
        seed_col = mapping.get(inferred_col, inferred_col)
        # limitation of resource
        # data_type = 'TEXT' #col['type']
        # cols.append(f'    cast("({seed_col}" as {data_type}) AS {inferred_col}')
        cols.append(f'    "{seed_col}" AS {inferred_col}')
    sql_lines.append(",\n".join(cols))
    sql_lines.append(f'FROM {{{{ ref("{seeds_name}") }}}}')
    return "\n".join(sql_lines)

def generate_schema_yml(tables, mapped_column, seeds_name):
    models = []
    for table in tables:
        cols = []
        for col in table['columns']:
            if col['name'] not in mapped_column:
                continue
            tests = ['not_null']
            if col['name'] in table['primary_key']:
                tests.append('unique')
            cols.append({
                'name': col['name'],
                'description': f"{col['description']}",
                'tests': tests
            })
        models.append({
            'name': table['table_name'],
            'description': f'Model that transforms the `{seeds_name}` seed into a standardized schema.',
            'columns': cols
        })
    return yaml.dump({'version': 2, 'models': models}, sort_keys=False)

def generate_dbt_project_yml(db_name, seeds_name):
    return yaml.dump({
        'name': db_name,
        'version': '1.0',
        'config-version': 2,
        'profile': db_name,
        'model-paths': ['models'],
        'seed-paths': ['seeds'],
        'models': {db_name: {'+materialized': 'table'}},
        'seeds': {seeds_name: {'+materialized': 'table', '+quote_columns': True}}
    }, sort_keys=False)

def generate_profiles_yml(db_name):
    return yaml.dump({
        db_name: {
            'target': 'dev',
            'outputs': {
                'dev': {
                    'type': 'duckdb',
                    'path': f"{db_name}.duckdb",
                    'schema': 'public'
                }
            }
        }
    }, sort_keys=False)

def dbt_generator(inferred_schema: dict, mapped_column: dict, seeds_name: str) -> dict:

    # init db
    database_name = inferred_schema['database_name']
    duckdb_client(database_name=database_name)

    models = {f"{table['table_name']}.sql": generate_sql_file(database_name, table, mapped_column, seeds_name)
            for table in inferred_schema['tables']}
    schema_yml = generate_schema_yml(inferred_schema['tables'], mapped_column, seeds_name)
    dbt_project_yml = generate_dbt_project_yml(inferred_schema['database_name'], seeds_name)
    profiles_yml = generate_profiles_yml(inferred_schema['database_name'])

    # OUTPUT RESULT
    dbt_construct = {
        "model": [models],
        "schema.yml": schema_yml,
        "dbt_project.yml": dbt_project_yml,
        "profiles.yml": profiles_yml
    }

    return dbt_construct
