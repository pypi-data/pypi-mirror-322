# Standard library imports
from datetime import datetime, timezone as dt_timezone
import json
import logging
from logging.handlers import RotatingFileHandler
import os
from typing import Optional, Union

TIMEZONE=datetime.now().astimezone().tzinfo

# class TimezoneFormatter(logging.Formatter):
#     """
#     Custom formatter to include timezone-aware timestamps in log messages.

#     Args:
#         fmt: The format string for the log message
#         datefmt: The format string for the timestamp
#         timezone: Optional specific timezone to use (defaults to local)

#     Example:
#         formatter = TimezoneFormatter(
#             fmt='%(asctime)s [%(timezone)s] %(levelname)s: %(message)s',
#             datefmt='%Y-%m-%d %H:%M:%S'
#         )
#     """

#     def __init__(
#         self,
#         fmt: Optional[str] = None,
#         datefmt: Optional[str] = None
#     ) -> None:
#         super().__init__(fmt, datefmt)
#         self.local_timezone = TIMEZONE

#     def formatTime(self, record: logging.LogRecord, datefmt: Optional[str] = None) -> str:
#         try:
#             local_dt = datetime.fromtimestamp(
#                 record.created, self.local_timezone)
#             if datefmt:
#                 return local_dt.strftime(datefmt)
#             else:
#                 return local_dt.isoformat()
#         except Exception as e:
#             raise RuntimeError(f"Failed to format time: {str(e)}") from e

#     def format(self, record: logging.LogRecord) -> str:
#         # Add timezone name to log record
#         record.timezone = str(self.local_timezone)
#         return super().format(record)


class CustomFormatter(logging.Formatter):
    def formatTime(self, record, datefmt):
        try:
            # Ensure datefmt is not None to avoid string concatenation errors
            if datefmt is None:
                datefmt = "%Y-%m-%d %H:%M:%S"  # Default time format
            
            # Create a timezone-aware datetime object
            tz_aware_time = datetime.fromtimestamp(record.created, tz=TIMEZONE)
            
            # Format the time with milliseconds
            formatted_time_with_ms = tz_aware_time.strftime(datefmt + ".%f")
            formatted_time = formatted_time_with_ms[:-3]  # Truncate to 3 decimal places for milliseconds
            
            # Get the timezone abbreviation (e.g., EST)
            timezone_abbr = tz_aware_time.strftime("%Z")
            
            # Combine the formatted time, milliseconds, and timezone
            return f"{formatted_time} {timezone_abbr}"
            
        except Exception as e:
            # Fallback to the parent class's default time formatting in case of errors
            return super().formatTime(record, datefmt)


def setup_logging(
    log_level: int = logging.DEBUG,
    log_file: Optional[str] = None,
    max_size_mb: int = 25,  # 25MB
    backup_count: int = 7,
    console_output: bool = True,
    log_format: Optional[str] = None,
    date_format: Optional[str] = None,
    json_format: bool = False,
    indent: Optional[int] = None
) -> logging.Logger:
    """
    Configure logging system with rotating file handler and optional console output.

    Args:
        log_level: Logging level (default: DEBUG)
        log_file: Log file path (default: app.log or app_json.log if json_format is True)
        max_size_mb: Max log file size in MB before rotation (default: 25MB)
        backup_count: Number of backup files to keep (default: 7)
        console_output: Enable console logging (default: True)
        log_format: Custom log format string (optional)
        date_format: Custom date format string (optional)
        json_format: Flag to determine if log format should be JSON (default: False)
        indent: Indentation level for JSON output (default: None)
    """
    try:
        if max_size_mb <= 0:
            raise ValueError("max_size_mb must be positive")
        if backup_count < 0:
            raise ValueError("backup_count must be non-negative")
        if indent is not None:
            if indent < 0:
                raise ValueError("indent must be non-negative")
            if not json_format:
                raise ValueError("indent parameter is only valid when json_format is True")

        # Validate log level
        valid_levels = {
            logging.DEBUG, logging.INFO, logging.WARNING,
            logging.ERROR, logging.CRITICAL
        }
        if log_level not in valid_levels:
            raise ValueError(f"Invalid log level: {log_level}. Valid levels are: {valid_levels}")
        
        # Validate the date_format
        if date_format:
            valid_codes = {"%Y", "%m", "%d", "%H", "%M", "%S", "%z", "%Z"}
            if not any(code in date_format for code in valid_codes):
                raise ValueError(f"Invalid date_format: {date_format} must contain at least one format code (e.g., %Y, %m, %H)")
            
        # Validate the log_format
        if log_format:
            valid_codes = {"%(asctime)s", "%(levelname)s", "%(name)s", "%(message)s"}
            if not any(code in log_format for code in valid_codes):
                raise ValueError(f"Invalid log_format: {log_format} must contain at least one format code (e.g., %(asctime)s, %(levelname)s)")

        # Calculate max file size in bytes
        max_bytes = max_size_mb * 1024 * 1024

        # Set default log file if not provided
        log_file = log_file or ("app_json.log" if json_format else "app.log")

        # Create log directory if it does not exist
        log_dir = os.path.dirname(log_file)
        if log_dir:  # If log_dir is not empty
            os.makedirs(log_dir, exist_ok=True)  # Create directory if it does not exist

            # check if the directory is writable
            test_file = os.path.join(log_dir, ".permission_test")
            try:
                with open(test_file, "w") as f:
                    f.write("test")
                os.remove(test_file)
            except IOError as e:
                raise PermissionError(f"Directory not writable: {log_dir}") from e

        # Check if log file is writable
        if os.path.exists(log_file):
            if not os.access(log_file, os.W_OK):
                raise PermissionError(f"File not writable: {log_file}")
            

    except Exception as e:  # Catch permission errors
        raise
    
    
    try:
        # Create logger
        logger = logging.getLogger(__name__)
        logger.setLevel(log_level)

        # Clear existing handlers
        logger.handlers = []

        # Set up formatter
        if json_format:
            formatter = logging.Formatter(json.dumps({
                "time": "%(asctime)s",
                "name": "%(name)s",
                "level": "%(levelname)s",
                "message": "%(message)s"
            }, indent=indent))
        else:
            formatter = CustomFormatter(
                log_format or "%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
                date_format or "%Y-%m-%d %H:%M:%S"
            )   

        # Set up file handler
        file_handler = RotatingFileHandler(
            log_file, maxBytes=max_bytes, backupCount=backup_count)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # Set up console handler if enabled
        if console_output:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)

        # Generate configuration details using get_config_message
        config_message = get_config_message(
            log_level=log_level,
            file_handler=file_handler,
            max_size_mb=max_size_mb,
            backup_count=backup_count,
            console_output=console_output,
            json_format=json_format,  # Adapt the format based on user preference
            indent=indent
        )

        # Log configuration details with respect to log_level
        if json_format:
            # Parse JSON as dictionary
            config_dict = json.loads(config_message)
            if log_level != 0:
                logger.log(log_level, {"Logging Configuration": config_dict})
            else:
                logger.warning({"Logging Configuration": config_dict})
        else:
            if log_level != 0:
                logger.log(log_level, (
                    f"Logging Configuration:\n"
                    f"{config_message}"
                ))
            else:
                logger.warning(f"Logging Configuration:\n{config_message}")

        return logger

    except Exception as e:
        raise RuntimeError(f"Failed to set up logging: {str(e)}") from e


def get_config_message(log_level, file_handler, max_size_mb, backup_count, console_output, json_format=False, indent=None):
    processID = os.getpid()

    if json_format:
        config_dict = {
            "Level": logging.getLevelName(log_level),
            "LogFile": file_handler.baseFilename,
            "MaxFileSizeMB": max_size_mb,
            "BackupCount": backup_count,
            "ConsoleOutput": console_output,
            "Timezone": str(TIMEZONE),
            "ProcessID": processID
        }
        return json.dumps(config_dict)
    else:
        return f"""
===============================
    Logging Configuration
===============================
Level        : {logging.getLevelName(log_level)}
Log File     : {file_handler.baseFilename}
Max File Size: {max_size_mb:.2f} MB
Backup Count : {backup_count}
Console Out  : {console_output}
Timezone     : {TIMEZONE}
ProcessID    : {processID}
===============================
"""


def get_logger(
    name: str = __name__,
    log_level: int = logging.DEBUG,
    log_file: Optional[str] = None,
    max_size_mb: int = 25,  # 25MB
    backup_count: int = 7,
    console_output: bool = True,
    log_format: Optional[str] = None,
    date_format: Optional[str] = None,
    json_format: bool = False,
    indent: Optional[int] = None
) -> logging.Logger:
    """
    Simplified function to set up logging and return a logger instance.

    Args:
        name: Name of the logger.
        log_level: Logging level.
        log_file: Log file name.
        max_size_mb: Max size of log file in MB before rotation.
        backup_count: Number of rotated backups to keep.
        console_output: Enable console logging (default: True)
        log_format: Custom log format string (optional)
        date_format: Custom date format string (optional)
        json_format: Flag to determine if log format should be JSON.
        indent: Indentation level for JSON output.

    Returns:
        logging.Logger: Configured logger instance.
    """
    return setup_logging(
        log_level=log_level,
        log_file=log_file,
        max_size_mb=max_size_mb,  # Pass max_size_mb parameter
        backup_count=backup_count,
        console_output=console_output,
        log_format=log_format,
        date_format=date_format,
        json_format=json_format,
        indent=indent
    )


# Example Usage
if __name__ == "__main__":
    try:
        logger = get_logger(console_output=True)
        logger.debug("Basic debug example")
        logger.info("Basic usage example")
        logger.info(datetime.now().astimezone().tzinfo)
        # JSON format example
        json_logger = get_logger(json_format=True, indent=2)
        json_logger.info("JSON format example")

        
    except Exception as e:
        print(f"Error: {str(e)}")
        raise
