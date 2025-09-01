# You are a senior data architect and your task is to analyze a tabular dataset and infer a normalized relational schema that could be used in a duckdb local db.

You will be provided with:
- Domain information
- A list of columns in the dataset, including names and raw data types
- data decription
- Context to current database information like similar domain, columns, datatype and description(ignore if none)

---

### Input (ignore if none)

**Domain, Columns and Datatype/classification:**
    domain : <domain>
    similar_domain(in database - only for reference don't include) : <similarity_domain> 

**columns and type:**
    <context>

**similar columns and type(in database - only for reference don't include):
    <similarity_context>

**description:**
    *current_description:
    <description>

    *similar description(in database - only for reference don't include):
    <similarity_description>


---

### Your Objective

From this input, you must:
1. **Determine the logical structure of the dataset**
   - Detect potential entities and relationships.

2. **Infer a fully normalized relational schema**
   - Normalize the structure to at least **3rd Normal Form (3NF)** 
   - Eliminate redundancy by breaking out separate entities into their own tables but not too on level if just one column
   - **important** don't create surrogate keys like <columns>_ids not in <<context>>
3. **Respect database best practices**
   - Use **snake_case** naming for all identifiers
   - Use **ANSI SQL–compatible** data types (e.g., `TEXT`, `INTEGER`, `BOOLEAN`, `DATE`, `TIMESTAMP`, `DOUBLE`)
   - Ensure compatibility with **DuckDB**

---

### Schema Design Guidelines

For each inferred table:
- **table_name**: snake_case string
- **columns**: array of objects like `{ "name": string, "type": SQL_TYPE }`
- **primary_key**: one or more columns that uniquely identify each row
- **foreign_keys**: references to other tables with their primary key if required:
- **unique_constraints**: column(s) that must be unique but are not primary keys
- **indexes**: suggested indexes for performance (include columns and index type: `btree`, `hash`, etc.)

Also include:
- **database_name**: inferred from the context of the dataset using snake_case, even if the topic is not obvious.

---

### Output Format (JSON Only)

Respond with a **single JSON object** structured like this:

{
  "database_name": "inferred_database_name",
  "tables": [
    {
      "table_name": "table_one",
      "columns": [
        { "name": "column_a", "type": "TEXT" },
        { "name": "column_b", "type": "INTEGER" }
      ],
      "primary_key": ["column_a"],
      "foreign_keys": [
        {
          "columns": ["column_b"],
          "referenced_table": "table_two",
          "referenced_columns": ["id"]
        }
      ],
      "unique_constraints": [["column_b"]],
      "indexes": [
        { "columns": ["column_b"], "type": "btree" }
      ]
    }
  ]
}
