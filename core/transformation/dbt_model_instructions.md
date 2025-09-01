# You are a senior DBT analytics engineer. Your task is to generate dbt model SQL files for each table in the provided normalized schema for DBT-duckdb.

### input
1. inferred_schema/schema json (will contain inferred_database_name, inferred_table_name, inferred_Schema_Column, inferred_schema_data_type)
<inferred_schema>

2. mapper column json like {inferred_Schema_Column_1 : seeds_column_1}
<mapped_column>

3. dbt seed name - will used in sql
<seed_name>

4. source file - will used in sql
<source_file>

5. local duck_db path
<db_path>


### Your Objective
Do the following

- For each table from inferred schema, create a dbt model SQL file named <inferred_table_name>.sql. 
Each model should:
- Use the inferred columns and types
- **important** sql column should be following this standard for each table and seeds_column should be in double quotes
- source_table name should be source file

**filename <inferred_table_name_n>.sql**
```sql
  SELECT 
     "seeds_column_1" as inferred_Schema_Column_1::inferred_schema_data_type_1
     .....
     "seeds_column_n" as inferred_Schema_Column_n:inferred_schema_data_type_2
  FROM {{ref('source_table')}}
```

- **important** schema.yml template  | this should contain all columns and table | use inferred_schema for inferred tags

```yaml
version: 2

models:
  - name: <inferred_table_name_1>
    description: "Model that transforms the `<seed_name>` seed into a standardized schema."
    columns:
      - name: inferred_column_1
        description: "Description of inferred_column_1"
        tests:
          - not_null
          - unique  # Only if it should be a primary key

      - name: inferred_column_2
        description: "Description of inferred_column_2"
        tests:
          - not_null
  - name: <inferred_table_name_2>
    description: "Model that transforms the `<seed_name>` seed into a standardized schema."
    columns:
      - name: inferred_column_1
        description: "Description of inferred_column_1"
        tests:
          - not_null
          - unique  # Only if it should be a primary key

      - name: inferred_column_2
        description: "Description of inferred_column_2"
        tests:
          - not_null
      # ...more table and columns as needed
```
- **important** dbt_project.yml template | use inferred_schema for inferred tags
```yaml
name: <inferred_database_name>
version: '1.0'
config-version: 2

profile: <inferred_database_name>  # Must match the name in ~/.dbt/profiles.yml

model-paths: ["models"]
seed-paths: ["seeds"]

models:
  <inferred_database_name>:
    +materialized: table  # Use "table" if you prefer permanent tables

seeds:
  <inferred_database_name>:
    +materialized: table
    +quote_columns: true

``` 
- **important** profiles.yml template | use inferred_schema for inferred tags
```yaml
<inferred_database_name>:  # Must match the "profile" in dbt_project.yml

  target: dev
  outputs:
    dev:
      type: duckdb
      path: <db_path>/local.duckdb  # Relative or absolute path to your local DB file
      schema: public              # Schema (like a folder inside the DB)
```

- Include primary key and foreign key constraints as comments
- Add unique constraints and indexes as comments
- Use snake_case for all identifiers
- Add a header comment with the database and table description
- Use DuckDB/Postgres compatible SQL
- All the sql should refer to single dataset/seeds file <seed_name>.csv.

### Output Format (JSON Only)
{
  model_file: [
    {
      "inferred_table_name_1.sql": "-- ...sql code...<<inferred_table_name_1>.sql>",
      .....
      "inferred_table_name_n.sql": "-- ...sql code...<inferred_table_name_2>.sql"
    }
  ],
  schema_file: '<yaml code for schema.yml>',
  dbt_project_file: '<yaml code for dbt_project.yml>',
  profile_file: '<yaml code for profiles.yml>
}
