"""
Enhances logging with additional context by defining the ContextLoggerAdapter class.

This module is designed to enrich logging output with contextual information, aiding in the distinction and understanding
of logs from various parts of an application or different instances. It includes the ContextLoggerAdapter class for this purpose"""

import json
import logging
import sys
from contextvars import ContextVar
from typing import Dict, Optional

from ds_toolkit.log.allowed_context import AllowedContext
from ds_toolkit.log.json_encoders import JsonEncoderDatetime
from ds_toolkit.log.validate_context import validate_context


class ContextLoggerAdapter(logging.LoggerAdapter):
    """
    A logging adapter that provides a unique instance based on the logger's name, allowing for context-specific logging.

    This adapter enhances the standard logging capabilities by allowing the inclusion of contextual information in log messages,
    making it easier to trace and understand logs from different parts of an application. It supports singleton-like behavior
    for instances with the same name, ensuring that only one instance exists for each unique logger name, unless different
    context or formatter arguments are provided.

    Attributes:
        _instances (Dict[str, "ContextLoggerAdapter"]): A class-level dictionary that stores instances of ContextLoggerAdapter
            by their names to ensure unique instances for each name.
        _record_factory_bak: Stores the original log record factory before it's potentially modified by this adapter.
            This allows for the restoration of the default behavior if needed.

    Methods:
        __new__: Creates or retrieves a ContextLoggerAdapter instance based on the logger's name.
        __init__: Initializes the adapter with a logger name, level, and optional context.
        _configure_logger: Configures the underlying logger with a name and level.
        replace_context: Replaces the current logging context with a new one.
        record_factory: Generates a log record, enriching it with the current context.
    """

    _instances: Dict[str, "ContextLoggerAdapter"] = {}  # Registry of instances by name
    _record_factory_bak = logging.getLogRecordFactory()

    def __new__(
        cls,
        name: str,
        level: Optional[str | int] = None,
        context: Optional[AllowedContext] = None,
    ) -> "ContextLoggerAdapter":
        """
        Create a new ContextLoggerAdapter instance or return an existing one.

        This method ensures that only one instance of ContextLoggerAdapter per name exists.
        If an instance with the given name already exists, it will return that instance.
        If `context` is provided and not None, it will update the existing instance with new context.
        Similarly, if `level` is provided, it will update the logging level of the existing instance.

        Parameters:
        - cls: The class.
        - name: The name of the logger adapter. Used to identify unique instances.
        - level: The logging level. Required on first initialisation.
        - context: Optional context information to be included in log messages.

        Returns:
        - An instance of ContextLoggerAdapter.
        """
        existing_instance = cls._instances.get(name)
        if existing_instance:
            if context is not None:
                existing_instance.replace_context(context)
            if level is not None:
                existing_instance.logger.setLevel(level)
                for handler in existing_instance.logger.handlers:
                    handler.setLevel(level)
            return existing_instance

        instance = super(ContextLoggerAdapter, cls).__new__(cls)
        cls._instances[name] = instance
        return instance

    def __init__(
        self,
        name: str,
        level: Optional[str | int] = None,
        context: Optional[AllowedContext] = None,
    ):
        """
        Initializes a ContextLoggerAdapter with a logger name, level, and optional context.

        This method configures the underlying logger, ensuring that the logger is ready for use
        with the specified context.

        Parameters:
            name (str): The name of the logger.
            level (Optional[str | int]): The logging level, either as a string (e.g., 'DEBUG') or an integer (logging.DEBUG).
            context (Optional[AllowedContext]): The context to include in log messages, if any.

        Raises:
            ValueError: If the context contains keys not allowed in AllowedContext.
        """
        if not hasattr(self, "_initialized"):
            if level is None:
                raise ValueError(
                    "Level is required when the instance is not initialized."
                )

            self._context = ContextVar(f"logging_context_{name}", default={})
            context = context if context is not None else {}
            self.replace_context(context)
            self._configure_logger(name, level)
            self._initialized = True

    def _configure_logger(self, name: str, level: str | int):
        """
        Configures the logger with the specified name and level.

        This method sets the logging level and ensures the logger has at least one handler. If no handlers are present,
        a new StreamHandler is added. If handlers exist, their level is updated.

        Parameters:
            name (str): The logger's name, typically a dot-separated hierarchical name.
            level (str | int): The logging level, either as a string (e.g., 'INFO') or an integer (logging.INFO).
        """
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter("[%(levelname)s] %(json_formatted)s")
        handler.setFormatter(formatter)
        handler.setLevel(level)

        self.logger: logging.Logger = logging.getLogger(name)
        self.logger.handlers = [handler]
        self.logger.setLevel(level)
        self.logger.propagate = False

        logging.setLogRecordFactory(self.record_factory)

    def add_context(self, additional_context: Optional[AllowedContext]):
        """
        Adds new context to the existing context.

        Parameters:
            additional_context (AllowedContext): The additional context to merge with existing context.
        """
        current_context = self._context.get()
        new_context = {**current_context, **additional_context}
        validate_context(new_context)
        self._context.set(new_context)

    def replace_context(self, new_context: Optional[AllowedContext]):
        """
        Replaces the current context with a new one, after validating it.

        Parameters:
            new_context (AllowedContext): The new context to set.
        """
        validate_context(new_context)
        self._context.set(new_context)

    def process(self, msg, kwargs):
        """Override process to use instance context"""
        kwargs["extra"] = self._context.get()
        return msg, kwargs

    def record_factory(self, *args, **kwargs) -> logging.LogRecord:
        """
        Custom record factory method that enhances the log record with JSON formatting.

        This method takes the standard log record generated by the logging library and
        adds a `json_formatted` attribute to it. This attribute contains a JSON string
        representation of the log message and any additional context provided. It uses
        a custom JSON encoder for datetime objects to ensure they are serialized properly.

        Additionally, to maintain the JSON format integrity in case of exceptions, this
        method clears the exception information from the log record. This prevents the
        logging library from printing the traceback in a non-JSON format, which could
        disrupt log parsing.

        Args:
            *args: Variable length argument list passed to the original record factory.
            **kwargs: Arbitrary keyword arguments passed to the original record factory.

        Returns:
            logging.LogRecord: The enhanced log record with a `json_formatted` attribute.
        """
        record: logging.LogRecord = self._record_factory_bak(*args, **kwargs)
        context = self._context.get()

        try:
            message = record.getMessage()
        except Exception as e:
            message = f"Error formatting log message: {str(e)}"

        record.json_formatted = json.dumps(
            {"message": message, **context},
            cls=JsonEncoderDatetime,
        )

        record.exc_info = None
        record.exc_text = None

        return record
