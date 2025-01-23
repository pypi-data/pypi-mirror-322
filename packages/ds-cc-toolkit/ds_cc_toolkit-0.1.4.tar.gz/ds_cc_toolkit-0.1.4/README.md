# DS-CC-TOOLKIT

DS-Toolkit is a comprehensive collection of resources tailored for Data Science Services. Developed with the aim of enhancing productivity and ensuring best practices in data science projects, this toolkit encapsulates a variety of utilities and frameworks.

## ContextLogger

### Info
The `ContextLoggerAdapter` provided by the DS-Toolkit is a context-aware lazy logger that offers several advantages over a regular logger.

1. **Efficient Logging**: The `ContextLoggerAdapter` is designed to be lazy, meaning that it defers the evaluation of log messages until they are actually emitted. This can significantly improve performance by avoiding unnecessary string formatting and evaluation of complex log messages when they are not needed.

2. **Contextual Logging**: The `ContextLoggerAdapter` allows you to easily include contextual information in your log messages. By providing a dictionary of key-value pairs as the last argument when creating the logger, you can include additional information such as IMEI, packet creation time, packet processed time, and truck ID. This can be extremely useful for troubleshooting and debugging purposes.

3. **Consistent Log Formatting**: The `ContextLoggerAdapter` uses the `Fmt` class for log message formatting. This class provides a convenient way to format log messages with placeholders and arguments, similar to the `str.format()` method. It ensures consistent and readable log message formatting across your codebase.

Overall, the `ContextLoggerAdapter` in the DS-Toolkit offers a powerful and efficient logging solution for data science projects. It combines lazy evaluation, contextual logging, flexible log levels, and consistent log formatting to enhance productivity and improve the debugging experience.

**IMPORTANT** DO NOT USE F-STRINGS AS IT DOES NOT SUPPORT LAZY LOGGING

### Example

```
from ds_toolkit.log import Fmt, ContextLoggerAdapter

LOGGING_LEVEL = logging.DEBUG
logger = ContextLoggerAdapter(
    "test_adapter",
    LOGGING_LEVEL,
    {
        "imei": "359206105981120",
        "runtime_created_at": "2021-09-01T12:00:00Z",
        "docket_id": "2",
        "truck_id": "1",
    }
)
logger.debug(
    Fmt(
        "fetching batch for device_data_{} between {} and {}",
        "359206105981120",
        "2024-07-09 08:35:42",
        "2024-07-09 08:45:42",
    )
) # log 1
logger.info("HELLO %s", "WORLD") # log 2
```


```
Log 1 output:
{
  "imei": "359206105981120",
  "runtime_created_at": "2021-09-01T12:00:00Z",
  "docket_id": "2",
  "truck_id": "1",
  "message": "fetching batch for device_data_359206105981120 between 2024-07-09 08:35:42 and 2024-07-09 08:45:42"
}
```
```
Log 2 output:
{
  "imei": "359206105981120",
  "runtime_created_at": "2021-09-01T12:00:00Z",
  "docket_id": "2",
  "truck_id": "1",
  "message": "HELLO WORLD"
}
```

Allowed context key-value pairs:
- imei: str | int
- runtime_created_at: str | datetime
- truck_id: str | int
- docket_id: str

## Development

### Getting Started

To get started with DS-CC-TOOLKIT, ensure you have Python 3.11 or higher installed. Follow these steps:

1. Clone the repository to your local machine.
2. Navigate to the project directory and install dependencies using Poetry (if you do not have Poetry installed on your machine then visit https://python-poetry.org/docs/ and follow instructions):

```sh
poetry install
```

3. Activate the Poetry shell to work within the virtual environment in your terminal:

```sh
poetry shell
```

4. Run pre-commit install to set up the git hook scripts:

```sh
pre-commit install
```

### Tests

To run tests ensure poetry is installed, shell is activated and you are at project root in terminal.
Following this scripts can be found in `pyproject.toml` to run dedicated tests, e.g:

```sh
poetry run test-unit
```
### Authors
Lukas Benic - lukas@cloudcycle.com
