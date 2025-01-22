# logging-bullet-train

A bullet-train style Python logging utility that enhances your logging output with colorful and emoji-enhanced messages for better readability and quicker debugging.

## Features

- **Colorful Log Levels**: Each log level is color-coded for immediate recognition.
- **Emoji Indicators**: Visual emojis represent different log levels, making logs more intuitive.
- **ISO Datetime Formatting**: Timestamps are formatted in ISO format for consistency.
- **Customizable**: Easily configurable to fit your project's needs.
- **Supports Multiple Environments**: Compatible with various environments and Python versions.

## Installation

You can install `logging-bullet-train` using `pip`:

```bash
pip install logging-bullet-train
```

For development purposes, use Poetry to install all dependencies:

```bash
poetry install
```

## Usage

Here's a simple example to get you started:

```python
import logging

import logging_bullet_train

# Set up the logger
logger = logging_bullet_train.set_logger("my_logger", level=logging.DEBUG)

# Log messages with different severity levels
logger.debug("This is a debug message")     # 🔎 DEBUG
logger.info("This is an info message")      # 💡 INFO
logger.warning("This is a warning message") # ⭐ WARNING
logger.error("This is an error message")    # 🚨 ERROR
logger.critical("This is a critical message")  # 🔥 CRITICAL
logger.log(1, "notset message")             # 🔘 UNKNOWN
```

**Sample Output:**

```
2024-12-21T08:08:12+00:00  🔎 DEBUG      my_logger:12  This is a debug message
2024-12-21T08:08:12+00:00  💡 INFO       my_logger:13  This is an info message
2024-12-21T08:08:12+00:00  ⭐ WARNING    my_logger:14  This is a warning message
2024-12-21T08:08:12+00:00  🚨 ERROR      my_logger:15  This is an error message
2024-12-21T08:08:12+00:00  🔥 CRITICAL   my_logger:16  This is a critical message
2024-12-21T08:08:12+00:00  🔘 UNKNOWN    my_logger:17  notset message
```

## Advanced Configuration

### Selecting an Emoji Theme

By default, the logger uses a set of emojis defined in the `default` theme:

- DEBUG: 🔎
- INFO: 💡
- WARNING: ⭐
- ERROR: 🚨
- CRITICAL: 🔥
- UNKNOWN: 🔘

Additional themes such as `fruit`, `weather`, and `night` are available in the source code. To switch themes, you can modify the formatter to use a different emoji mapping. For example:

```python
from logging_bullet_train import level_emoji_fruit, BulletTrainFormatter, set_logger

class FruitBulletTrainFormatter(BulletTrainFormatter):
    def format(self, record):
        # Override emoji selection to use fruit theme
        level = record.levelno
        emoji = level_emoji_fruit.get(level, level_emoji_fruit[logging_bullet_train.LOGGING_UNKNOWN])
        record.levelname = f"{emoji} {record.levelname}"
        return super().format(record)

# Set up the logger with the custom formatter
logger = logging.getLogger("fruit_logger")
handler = logging.StreamHandler()
handler.setFormatter(FruitBulletTrainFormatter())
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

logger.info("This info message uses fruit emojis")
```

### Customizing Colors and Formatting

The logger supports customization of colors and formatting. You can adjust color schemes or extend the formatter to better suit your needs by modifying the color dictionaries or overriding the `BulletTrainFormatter` methods.

```python
from logging_bullet_train import set_logger, wrap_text, Fore, Back

# Set up a custom logger
custom_logger = set_logger("custom_logger", level=logging.DEBUG)

# Use custom color styling in your messages if needed
message = wrap_text("Custom styled message", fg=Fore.CYAN, bg=Back.BLACK)
custom_logger.info(message)
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
