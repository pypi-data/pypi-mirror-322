"""
This module provides custom JSON encoders designed to enhance the default json.JSONEncoder by handling non-serializable objects and datetime objects.

Classes:
    JsonEncoderStrFallback: Extends json.JSONEncoder to convert non-serializable objects to strings, preventing serialization errors.
    JsonEncoderDatetime: Inherits from JsonEncoderStrFallback and adds functionality to serialize datetime objects into string representations.
"""

import json
from datetime import datetime


class JsonEncoderStrFallback(json.JSONEncoder):
    """
    A JSON encoder that falls back to converting non-serializable objects to strings.
    """

    def default(self, obj):
        try:
            return super().default(obj)
        except TypeError as exc:
            if "not JSON serializable" in str(exc):
                return str(obj)
            raise


class JsonEncoderDatetime(JsonEncoderStrFallback):
    """
    A JSON encoder that handles datetime objects, converting them to a string representation.
    Inherits from JsonEncoderStrFallback to handle non-serializable objects by converting them to strings.
    """

    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%dT%H:%M:%S%z")

        return super().default(obj)
