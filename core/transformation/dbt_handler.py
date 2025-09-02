import os
from typing import Dict, Any, Tuple
from core.inference_client import get_chat_completion
from core.data_reader import read, input_path
from core.transformation.dbt_generator import dbt_generator


dbt_model_instructions_path = 'core/transformation/dbt_model_instructions.md'


def seed_mapper(inferred_schema: Dict[str, Any]) -> Tuple[Dict, str]:
    seeds_columns = ','.join(read(input_path()).columns.to_list())
    seeds_name = os.path.basename(input_path()).split('.')[0]

    instruction = '''
    You are a data modeller, your task is to map matching column from given input inferred_schema json to csv file column and if not found then NONE.

    input:
    1. inferred schema json (by LLM)
        <inferred_schema>
    2. dbt seeds column (given in csv file source)
        <seeds_columns>

    your objective:
    1. for each inferred_schema column find seeds_column from given seeds_columns else assign NONE

    output (json only)
    {
        inferred_Schema_Column_1 : seeds_column_1 <None if not found>,
        ....
        inferred_Schema_Column_n : seeds_column_n,
    }
    '''

    mapped_columns = get_chat_completion(instruction.replace('<inferred_schema>', str(inferred_schema)).replace('<seeds_columns>', seeds_columns))
    
    # Remove none mapped columns
    if isinstance(mapped_columns, dict):
        mapped_columns = {k: v for k, v in mapped_columns.items() if v is not None}

    return (mapped_columns, seeds_name)
    


def create_dbt_model(inferred_schema: Dict[str, Any]) -> None:
    """
    Generate dbt model SQL files from inferred schema using LLM and save to transformation folder.
    """

    mapped_columns, seeds_name = seed_mapper(inferred_schema)

    dbt_construct = dbt_generator(inferred_schema, mapped_columns, seeds_name)

    output_dir = os.path.join(os.path.dirname(__file__), 'dbt_files', inferred_schema['database_name'])
    os.makedirs(output_dir, exist_ok=True)

    for filename, construct in dbt_construct.items():
        if filename == 'model':
            for sql in construct:
                for sql_file, sql_code in sql.items():
                    # create model directory if not exists
                    model_dir = os.path.join(output_dir, 'models')
                    os.makedirs(model_dir, exist_ok=True)
                    file_path = os.path.join(output_dir, 'models', sql_file)
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(sql_code)
        elif filename == 'schema.yml':
            schema_dir = os.path.join(output_dir, 'models')
            os.makedirs(schema_dir, exist_ok=True)
            file_path = os.path.join(schema_dir, 'schema.yml')
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(construct)
        else:
            file_path = os.path.join(output_dir, filename)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(construct)
    # Call dbt_executor to run dbt commands and open docs
    from core.transformation import dbt_executor
    dbt_executor.execute_all(inferred_schema['database_name'])
