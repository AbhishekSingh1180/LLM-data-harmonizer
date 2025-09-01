# You are an expert data analyst.

Given the following sample data from a dataset:

### input
Columns from sample data 
<columns>

Records from sample data in respective order of columns above
<records>

### Your Objective
Please provide:
1. The most likely domain or topic of the dataset (e.g. healthcare, finance, retail).
2. a short description about the data
3. A classification of each given column by semantic data type/category (e.g. name, date, currency, category, identifier).


### Output Format (JSON Only)
Please respond ONLY with a valid JSON object with this structure:

{{
  "domain": "string",
  "description": "string",
  "columns": {{
    "ColumnName1": "type1",
    "ColumnName2": "type2",
    ...
  }}
}}

