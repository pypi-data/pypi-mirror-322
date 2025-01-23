"""
ContextValidator is class used for validating a context dictionary against a predefined set of allowed keys.
It ensures that the context contains all required keys, only contains allowed keys, and does not have duplicate values.
"""

from ds_toolkit.log.allowed_context import AllowedContext


def validate_context(context):
    """
    Validates that each key in the input context is an allowed key.

    Parameters:
        context (Dict[str, Any]): The context dictionary to validate.

    Raises:
        ValueError: If any key in the context is not in AllowedContext.
    """
    if context is None:
        return

    allowed_keys: set = set(AllowedContext.__annotations__.keys())
    invalid_keys = [key for key in context.keys() if key not in allowed_keys]
    if invalid_keys:
        raise ValueError(
            f"Context contains invalid keys: {', '.join(sorted(invalid_keys))}"
        )
