"""Файл, в котором содержатся схемы для валидации json-объекта."""
schema_post_order = {
        "type": "object",
        "required": [
            "address_from", "address_to", "client_id", "driver_id", "date_created", "status"
        ],
        "additionalProperties": False,
        "properties": {
            "address_from": {
                "type": "string"
            },
            "address_to": {
                "type": "string"
            },
            "client_id": {
                "type": "integer"
            },
            "driver_id": {
                "type": "integer"
            },
            "date_created": {
                "type": "string"
            },
            "status": {
                "type": "string"
            }
        }
    }
schema_id = {
        "type": "object",
        "required": [
            "id"
        ],
        "additionalProperties": False,
        "properties": {
            "id": {
                "type": "integer"
            }

            }
        }
schema_put_order = {
        "type": "object",
        "required": [
            "id", "address_from", "address_to", "client_id", "driver_id", "date_created", "status"
        ],
        "additionalProperties": False,
        "properties": {
            "id": {
                "type": "integer"
            },
            "address_from": {
                "type": "string"
            },
            "address_to": {
                "type": "string"
            },
            "client_id": {
                "type": "integer"
            },
            "driver_id": {
                "type": "integer"
            },
            "date_created": {
                "type": "string"
            },
            "status": {
                "type": "string"
            }
        }
    }
schema_post_driver = {
        "type": "object",
        "required": [
            "name", "car"
        ],
        "additionalProperties": False,
        "properties": {
            "name": {
                "type": "string"
            },
            "car": {
                "type": "string"
            }
        }
    }
schema_post_client = {
        "type": "object",
        "required": [
            "name", "is_vip"
        ],
        "additionalProperties": False,
        "properties": {
            "name": {
                "type": "string"
            },
            "is_vip": {
                "type": "integer"  # так как для запроса в Postman используются числа 1 для True и 0 для False
            }
        }
    }
