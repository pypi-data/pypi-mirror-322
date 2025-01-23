"""Logging definitions."""
import logging
import typing

import colorlog


def configure_logging(verbose: int, log_file: str) -> None:
    """Configure logging for both import and gen-data scripts."""
    # Define TRACE level
    logging.TRACE = 5  # type: ignore
    logging.addLevelName(logging.TRACE, "TRACE")  # type: ignore

    def trace(self: logging.Logger, message: object, *args: typing.Any, **kws: typing.Any) -> None:
        if self.isEnabledFor(logging.TRACE):  # type: ignore
            self._log(logging.TRACE, message, args, **kws)  # type: ignore # pylint: disable=protected-access

    logging.Logger.trace = trace  # type: ignore

    # Get root logger
    root = logging.getLogger()

    # Define formatter for file logging.
    fmt = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')

    # Define formatter for colored console logging.
    color_fmt = colorlog.ColoredFormatter(
        '%(log_color)s%(asctime)s %(levelname)-8s %(message)s',
        log_colors={
            'TRACE': 'light_cyan',
            'DEBUG': 'light_yellow',
            'INFO': 'light_green',
            'WARNING': 'light_purple',
            'ERROR': 'light_red',
            'CRITICAL': 'light_red'
        }
    )

    # Define console handler
    color_handler = colorlog.StreamHandler()
    color_handler.setFormatter(color_fmt)
    root.addHandler(color_handler)

    # Set log file
    if log_file is not None:
        fh = logging.FileHandler(log_file)
        fh.setFormatter(fmt)
        root.addHandler(fh)

    # Set log level
    if verbose > 2:
        root.setLevel(logging.TRACE)  # type: ignore
    elif verbose == 2:
        root.setLevel(logging.DEBUG)
    elif verbose == 1:
        root.setLevel(logging.INFO)
