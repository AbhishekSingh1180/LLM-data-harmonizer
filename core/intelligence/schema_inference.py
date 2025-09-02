
from core.inference_client import get_chat_completion
from core.data_reader import read
from pprint import pprint

schema_inference_instructions_path = 'core/intelligence/schema_inference.md'
mmd_inference_instructions_path = 'core/intelligence/mmd_inference.md'


def generate_and_save_mermaid_mmd(schema_json, output_path='ERD/erd.mmd'):
    """
    Generate a Mermaid ER diagram (mmd code) from a schema JSON and save it to a file.
    """
    mmd_instructions: str = read(mmd_inference_instructions_path)

    instruction = mmd_instructions
    replacements = {
        "<schema>": str(schema_json)
    }
    for tag, value in replacements.items():
        instruction = instruction.replace(tag, value)
    
    mmd_result = get_chat_completion(instruction)
    mmd_code = mmd_result.get('mmd', '')
    with open(output_path, 'w') as f:
        f.write(mmd_code)


# def schema_inference(context: dict) -> dict:
def schema_inference(data_context: dict) -> dict:
    """Infer a detailed schema based on the classified schema context."""
    schema_inference_instruction: str = read(schema_inference_instructions_path)

    instruction = schema_inference_instruction
    replacements = {
        "<domain>": str(data_context.get('domain', '')),
        "<similarity_domain>": str(data_context.get('similarity_domain', '')),
        "<context>": str(data_context.get('context', '')),
       # "<similarity_context>": str(data_context.get('similarity_context', '')),
        "<description>": str(data_context.get('description', '')),
        "<similarity_description>": str(data_context.get('similarity_description', ''))
    }
    for tag, value in replacements.items():
        instruction = instruction.replace(tag, value)

    query_result = get_chat_completion(instruction)

    pprint(query_result)

    generate_and_save_mermaid_mmd(query_result)
    return query_result
