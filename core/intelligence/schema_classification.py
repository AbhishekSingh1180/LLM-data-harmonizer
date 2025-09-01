import pandas as pd
import os
from core.inference_client import get_chat_completion
from core.data_reader import read, input_path
from core.storage.vector_store import VectorStoreClient
from pprint import pprint

schema_classification_instructions_path = 'core/intelligence/schema_classification.md'
vector_client = VectorStoreClient(collection_name="schema_classification")


def get_column_and_types(data: pd.DataFrame) -> str:
    """Get the data types of each column"""
    data_dict = data.dtypes.astype(str).to_dict()
    column_types = " | ".join([f"{col}: {col_type}"
                              for col, col_type in data_dict.items()])
    return column_types


def get_sample_data(data: pd.DataFrame, n: int = 1) -> str:
    """Get a sample of the data."""
    data_head = data.head(n)
    sample_data = '\n'.join(','.join(map(str, row))
                            for row in data_head.values)
    return sample_data


def schema_classification_to_text(query: dict) -> str:
    """Flatten schema classification dict into a string for embedding."""
    domain = query.get("domain", "")
    description = query.get("description", "")
    columns = query.get("columns", {})
    column_combined = " | ".join([f"{col}: {col_type}" for col, col_type in columns.items()])
    return f"Domain: {domain}\nDescription: {description}\nColumns: {column_combined}"


def schema_classification() -> dict:
    """Classify the schema of the given DataFrame."""
    source_file = os.path.basename(input_path())
    data: pd.DataFrame = read(input_path())

    column_and_types = get_column_and_types(data)
    sample_data = get_sample_data(data)
    classification_instruction: str = read(schema_classification_instructions_path)

    instruction = classification_instruction
    replacements = {
        "<columns>": column_and_types,
        "<records>": sample_data
    }
    for key, value in replacements.items():
        instruction = instruction.replace(key, value)
    query_result = get_chat_completion(instruction)

    similarity_search = vector_client.query(query=query_result, query_to_text_fn=schema_classification_to_text)

    # pprint(similarity_search)

    if (similarity_search['distances'][0] and len(similarity_search['distances'][0]) > 0 and similarity_search['distances'][0][0] < 0.5):
        print(f"Similar schema found with distance {similarity_search['distances'][0][0]}. Not adding new schema.")
        print("Similar schema metadata:", similarity_search['metadatas'][0][0])

        return {
            'similarity_flag': True,
            'similarity_domain': [similarity_search['metadatas'][0][0]['domain']],
            'domain': [query_result['domain']],
            'similarity_description': [similarity_search['metadatas'][0][0]['description']],
            'description': [query_result['description']],
            'similarity_context': similarity_search['documents'][0],
            'context': [schema_classification_to_text(query_result)]
        }

    vector_client.store_embeddings(
        query=query_result,
        query_to_text_fn=schema_classification_to_text
    )

    return {
        'similarity_flag': False,
        'similarity_domain': None,
        'domain': [query_result['domain']],
        'similarity_description': None,
        'description': [query_result['description']],
        'similarity_context': None,
        'context': [schema_classification_to_text(query_result)]
    }
