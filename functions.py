"""Файл, в котором содержатся вспомогательные функции."""
import jsonschema


def valid_json(dict_json: dict, schema: dict) -> bool:
    """Валидация json-объекта."""
    try:
        jsonschema.validate(instance=dict_json, schema=schema)
    except jsonschema.ValidationError:
        return False
    return True
