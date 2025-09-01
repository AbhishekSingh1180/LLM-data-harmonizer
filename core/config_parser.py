import configparser
import os
from typing import Union
import inspect


def read_config(filepath: Union[str, os.PathLike]) -> dict:
    caller_module = os.path.basename(inspect.stack()[1].filename).split('.')[0]

    section: str = {
        'inference_client': 'inference'
    }.get(caller_module, 'other')

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Config file not found: {filepath}")
    _, ext = os.path.splitext(filepath)
    if ext != '.cfg':
        raise ValueError("Unsupported config file format. Use .cfg")
    config = configparser.ConfigParser()
    config.read(filepath)
    if section not in config:
        raise ValueError(f"Section '{section}' not found in config file.")
    return {key: value for key, value in config.items(section)}
