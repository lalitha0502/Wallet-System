from dataclasses import fields

def map_to_dataclass(model, row: dict):
    model_fields = {f.name for f in fields(model)}
    filtered = {k: v for k, v in row.items() if k in model_fields}
    return model(**filtered)