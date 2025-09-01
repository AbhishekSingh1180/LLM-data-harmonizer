from core.intelligence.schema_classification import schema_classification
from core.intelligence.schema_inference import schema_inference
from core.transformation.dbt_handler import create_dbt_model
from pprint import pprint


def main():
    """
    Main entry point for the application.
    Initializes the schema classification context and orchestrates the primary
    workflow of the LLM-Data-Harmonizer.
    """
    classification_context: dict = schema_classification()
    inferred_schema: dict = schema_inference(data_context=classification_context)
    create_dbt_model(inferred_schema)

if __name__ == "__main__":
    main()
