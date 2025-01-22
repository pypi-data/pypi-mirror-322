import datetime
import logging
import os
import typing
import zoneinfo

import tzlocal
from colorama import Back, Fore, Style

LOGGING_UNKNOWN = 1
logging.addLevelName(LOGGING_UNKNOWN, "UNKNOWN")

level_emoji_default = {
    logging.DEBUG: "🔎",
    logging.INFO: "💡",
    logging.WARNING: "⭐",
    logging.ERROR: "🚨",
    logging.CRITICAL: "🔥",
    LOGGING_UNKNOWN: "🔘",
}
level_emoji_fruit = {
    logging.DEBUG: "🫐",
    logging.INFO: "🍏",
    logging.WARNING: "🍋",
    logging.ERROR: "🍒",
    logging.CRITICAL: "🌶️",
    LOGGING_UNKNOWN: "🍇",
}
level_emoji_weather = {
    logging.DEBUG: "🌤️",
    logging.INFO: "☀️",
    logging.WARNING: "🌦️",
    logging.ERROR: "⛈️",
    logging.CRITICAL: "🌪️",
    LOGGING_UNKNOWN: "🌈",
}
level_emoji_night = {
    logging.DEBUG: "🌑",
    logging.INFO: "🌓",
    logging.WARNING: "🌕",
    logging.ERROR: "🌠",
    logging.CRITICAL: "☄️",
    LOGGING_UNKNOWN: "🌌",
}
level_emojis = {
    "default": level_emoji_default,
    "fruit": level_emoji_fruit,
    "weather": level_emoji_weather,
    "night": level_emoji_night,
}


type BACK_ARROW = typing.Tuple[typing.Text | None, typing.Text | None]

datetime_color: BACK_ARROW = (Back.WHITE, Fore.WHITE)
levelname_color: typing.Dict[int, BACK_ARROW] = {
    logging.DEBUG: (Back.BLUE, Fore.BLUE),
    logging.INFO: (Back.GREEN, Fore.GREEN),
    logging.WARNING: (Back.YELLOW, Fore.YELLOW),
    logging.ERROR: (Back.RED, Fore.RED),
    logging.CRITICAL: (Back.MAGENTA, Fore.MAGENTA),
    LOGGING_UNKNOWN: (Back.BLACK, Fore.BLACK),
}
logger_name_color: typing.Dict[int, BACK_ARROW] = {
    logging.DEBUG: (Back.LIGHTBLUE_EX, Fore.LIGHTBLUE_EX),
    logging.INFO: (Back.LIGHTGREEN_EX, Fore.LIGHTGREEN_EX),
    logging.WARNING: (Back.LIGHTYELLOW_EX, Fore.LIGHTYELLOW_EX),
    logging.ERROR: (Back.LIGHTRED_EX, Fore.LIGHTRED_EX),
    logging.CRITICAL: (Back.LIGHTMAGENTA_EX, Fore.LIGHTMAGENTA_EX),
    LOGGING_UNKNOWN: (Back.LIGHTBLACK_EX, Fore.LIGHTBLACK_EX),
}
msg_color: typing.Dict[int, typing.Text | None] = {
    logging.DEBUG: None,
    logging.INFO: Fore.GREEN,
    logging.WARNING: Fore.YELLOW,
    logging.ERROR: Fore.RED,
    logging.CRITICAL: Fore.MAGENTA,
    LOGGING_UNKNOWN: None,
}


def to_level(
    levelname: typing.Text | int,
) -> typing.Literal[1, 10, 20, 30, 40, 50]:
    if isinstance(levelname, typing.Text):
        levelname = levelname.upper()
        if levelname == "DEBUG":
            return logging.DEBUG  # type: ignore
        elif levelname == "INFO":
            return logging.INFO  # type: ignore
        elif levelname == "WARNING":
            return logging.WARNING  # type: ignore
        elif levelname == "ERROR":
            return logging.ERROR  # type: ignore
        elif levelname == "CRITICAL":
            return logging.CRITICAL  # type: ignore
        else:
            return LOGGING_UNKNOWN  # type: ignore
    else:
        if levelname >= logging.CRITICAL:
            return logging.CRITICAL  # type: ignore
        elif levelname >= logging.ERROR:
            return logging.ERROR  # type: ignore
        elif levelname >= logging.WARNING:
            return logging.WARNING  # type: ignore
        elif levelname >= logging.INFO:
            return logging.INFO  # type: ignore
        elif levelname >= logging.DEBUG:
            return logging.DEBUG  # type: ignore
        else:
            return LOGGING_UNKNOWN  # type: ignore


def wrap_text(
    text: typing.Text, *, fg: typing.Text | None = None, bg: typing.Text | None = None
) -> typing.Text:
    fg_str = fg or ""
    bg_str = bg or ""
    return f"{bg_str}{fg_str}{text}{Style.RESET_ALL}"


class IsoDatetimeFormatter(logging.Formatter):
    def formatTime(
        self, record: logging.LogRecord, datefmt: typing.Literal[None] = None
    ):
        record_datetime = datetime.datetime.fromtimestamp(record.created).astimezone(
            self._get_local_timezone()
        )
        # Drop microseconds
        record_datetime = record_datetime.replace(microsecond=0)
        return record_datetime.isoformat()

    def _get_local_timezone(self) -> zoneinfo.ZoneInfo:
        """
        Attempt to fetch the time zone from the TZ environment variable.
        If missing or invalid, fall back to the system local zone,
        and if that fails, default to UTC.
        """
        tz_env = os.getenv("TZ")
        if tz_env and tz_env.strip():
            try:
                return zoneinfo.ZoneInfo(tz_env.strip())
            except Exception:
                pass
        # Fallback: system local zone or UTC
        try:
            return tzlocal.get_localzone()
        except Exception:
            return zoneinfo.ZoneInfo("UTC")


class BulletTrainFormatter(IsoDatetimeFormatter):
    def format(self, record: logging.LogRecord):
        arrow = "\uE0B0"
        ts = self.formatTime(record)
        level = to_level(record.levelno)
        levelname = record.levelname
        emoji = level_emoji_default[level]
        levelname_with_emoji = f"{emoji} {levelname}"
        msg_ = record.getMessage()
        time_color = datetime_color
        level_color = levelname_color[level]
        name_color = logger_name_color[level]
        msg_color_ = msg_color[level]
        log_line = ""

        # Time
        time_colored = wrap_text(f" {ts} ", bg=time_color[0])
        time_out_arrow = wrap_text(arrow, fg=time_color[1], bg=level_color[0])
        log_line += f"{time_colored}{time_out_arrow}"

        # Logger level
        level_colored = wrap_text(f" {levelname_with_emoji:10s} ", bg=level_color[0])
        level_out_arrow = wrap_text(arrow, fg=level_color[1], bg=name_color[0])
        log_line += f"{level_colored}{level_out_arrow}"

        # Logger name
        name_colored = wrap_text(f" {record.name}:{record.lineno} ", bg=name_color[0])
        name_out_arrow = wrap_text(arrow, fg=name_color[1])
        log_line += f"{name_colored}{name_out_arrow}"

        # Message
        message_colored = wrap_text(f" {msg_}", fg=msg_color_)
        if record.exc_info:
            message_colored += "\n" + self.formatException(record.exc_info)
        log_line += message_colored

        # Output the log line
        return log_line


def set_logger(
    logger: logging.Logger | typing.Text,
    *,
    level: int = logging.DEBUG,
) -> logging.Logger:
    logger = logging.getLogger(logger) if isinstance(logger, typing.Text) else logger
    handler = logging.StreamHandler()
    formatter = BulletTrainFormatter()
    handler.setFormatter(formatter)
    handler.setLevel(level)
    logger.addHandler(handler)
    logger.setLevel(level)
    return logger


if __name__ == "__main__":
    logger = set_logger("sdk", level=logging.DEBUG)
    logger.debug("debug message")
    logger.info("info message")
    logger.warning("warning message")
    logger.error("error message")
    logger.critical("critical message")
    logger.log(1, "notset message")
