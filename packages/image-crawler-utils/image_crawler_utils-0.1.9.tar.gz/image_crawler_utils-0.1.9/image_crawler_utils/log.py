import os, sys
from typing import Optional, Union

import logging, getpass
import rich
from rich.logging import RichHandler

from image_crawler_utils.configs import DebugConfig



##### Initialization


logging.basicConfig(
    level=logging.NOTSET,
    handlers=[],
)

__rich_handler = RichHandler(
    log_time_format='[%X]',
    show_path=False,
)
__rich_handler.setFormatter(logging.Formatter('%(message)s'))
__rich_handler.setLevel(logging.NOTSET)
__rich_logger = logging.getLogger("Console")
__rich_logger.addHandler(__rich_handler)


##### Log utils


def print_logging_msg(
        msg: str,
        level: str='',
        debug_config: DebugConfig=DebugConfig.level("debug"),
    ):
    """
    Print time and message according to its logging level.
    If debug_config is used and the logging level is not allowed to show, the message will not be output.
    
    Parameters:
        level (str): Level of messages.
            - Should be one of "debug", "info", "warning", "error", "critical".
            - Set it to other string or leave it blank will always output msg string without any prefix.
        msg (str): The message string to output.
        debug_config (image_crawler_utils.configs.DebugConfig): DebugConfig that controls output level. Default set to debug-level (output all).
    """
    
    if level.lower() == 'debug':
        if debug_config.show_debug:
            __rich_logger.debug(msg)
    elif level.lower() == 'info':
        if debug_config.show_info:
            __rich_logger.info(msg)
    elif level.lower() == 'warning' or level.lower() == 'warn':
        if debug_config.show_warning:
            __rich_logger.warning(msg)
    elif level.lower() == 'error':
        if debug_config.show_error:
            __rich_logger.error(msg)
    elif level.lower() == 'critical':
        if debug_config.show_critical:
            __rich_logger.critical(msg)
    else:
        rich.print(msg)


class Log:
    def __init__(
            self, 
            log_file: Optional[str]=None,
            debug_config: DebugConfig=DebugConfig(),
            logging_level: Union[str, int]=logging.DEBUG,
            detailed_console_log: bool=False,
        ):
        """
        Logging messages.

        Parameters:
            log_file (str): Output name for the logging file. NO SUFFIX APPENDED. Set to None (Default) is not to output any file.
            debug_config (image_crawler_utils.configs.DebugConfig): Set the OUTPUT MESSAGE TO CONSOLE level. Default is not to output any message.
            logging_level (str or int): Set the logging level of the LOGGING FILE.
                - Select from: logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR and logging.CRITICAL
            detailed_console_log (bool): When logging info to the console, always log `msg` (the messages logged into files) even if `output_msg` exists.
        """

        self.debug_config = debug_config
        self.detailed_console_log = detailed_console_log

        self.logger = logging.getLogger(getpass.getuser())
        self.logger.setLevel(logging_level)

        self.formatter = logging.Formatter('%(asctime)-12s %(levelname)-8s %(message)-12s')

        # Don't write to console; We have better output method.
        self.empty_stream_handler = logging.StreamHandler(stream=sys.stdout)
        self.empty_stream_handler.setLevel(logging.CRITICAL + 1)
        self.logger.addHandler(self.empty_stream_handler)

        # Write to file
        self.file_handler = None

        if log_file is not None:
            path, filename = os.path.split(log_file)
            self.filename = f"{filename}.log".replace(".log.log", ".log")

            if len(path) > 0 and not os.path.exists(path):
                os.makedirs(path)
            self.log_file = os.path.join(path, self.filename)
            self.file_handler = logging.FileHandler(
                filename=self.log_file,
                encoding='UTF-8'
            )
            self.file_handler.setFormatter(self.formatter)
            self.file_handler.setLevel(logging_level)
            self.logger.addHandler(self.file_handler)

    # Check whether logging to file
    def logging_file_handler(self):
        """
        Return the file handler if logging into file, or None if not.
        """

        return self.file_handler is not None
    
    # Output .log path
    def logging_file_path(self):
        """
        Output the absolute path of logging file if exists, or None if not.
        """

        if self.logging_file_handler():
            return os.path.abspath(self.log_file)
        else:
            return None

    # Five levels of logging
    # msg will be recorded in logging file
    # output_msg will be printed on console instead of msg if it isn't None.
    def debug(self, msg: str, output_msg: Optional[str]=None):
        """
        Output debug messages.

        Parameters:
            msg (str): Logging message.
            output_msg (str or None): Message to be output to console. Set to None will output the string in `msg` parameter.
        """

        self.logger.debug(msg)
        print_logging_msg(output_msg if (output_msg is not None and not self.detailed_console_log) else msg, "debug", self.debug_config)
        return msg

    def info(self, msg: str, output_msg: Optional[str]=None):
        """
        Output info messages.

        Parameters:
            msg (str): Logging message.
            output_msg (str or None): Message to be output to console. Set to None will output the string in `msg` parameter.
        """
        
        self.logger.info(msg)
        print_logging_msg(output_msg if (output_msg is not None and not self.detailed_console_log) else msg, "info", self.debug_config)
        return msg

    def warning(self, msg: str, output_msg: Optional[str]=None):
        """
        Output warning messages.

        Parameters:
            msg (str): Logging message.
            output_msg (str or None): Message to be output to console. Set to None will output the string in `msg` parameter.
        """
        
        self.logger.warning(msg)
        print_logging_msg(output_msg if (output_msg is not None and not self.detailed_console_log) else msg, "warning", self.debug_config)
        return msg

    def error(self, msg: str, output_msg: Optional[str]=None):
        """
        Output error messages.

        Parameters:
            msg (str): Logging message.
            output_msg (str or None): Message to be output to console. Set to None will output the string in `msg` parameter.
        """
        
        self.logger.error(msg)
        print_logging_msg(output_msg if (output_msg is not None and not self.detailed_console_log) else msg, "error", self.debug_config)
        return msg

    def critical(self, msg: str, output_msg: Optional[str]=None):
        """
        Output critical messages.

        Parameters:
            msg (str): Logging message.
            output_msg (str or None): Message to be output to console. Set to None will output the string in `msg` parameter.
        """
        
        self.logger.critical(msg)
        print_logging_msg(output_msg if (output_msg is not None and not self.detailed_console_log) else msg, "critical", self.debug_config)
        return msg
    