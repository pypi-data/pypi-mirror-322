import os

prefix = "LUNAR_VAR_"


def variable(key):
    for key, value in os.environ.items():
        if key.startswith(prefix):
            trimmed_key = key[len(prefix):]  # Remove prefix
            if trimmed_key == key:
                return value

    return None


def variable_or_default(key, default):
    value = variable(key)
    if value is None:
        return default
    return value
