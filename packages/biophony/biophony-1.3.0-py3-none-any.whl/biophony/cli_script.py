"""Module for abstract CLI code."""

import abc
import argparse
import logging
import sys
import traceback

from .logger import configure_logging

logger = logging.getLogger("biophony")


class CliScript(abc.ABC):
    """Abstract CLI mother class.

    :param desc: The script description that will appear on the help page.
    """

    def __init__(self, desc: str) -> None:
        self._desc = desc

    @abc.abstractmethod
    def declare_args(self, p: argparse.ArgumentParser) -> None:
        """Declares custom command line arguments for the script."""
        raise NotImplementedError

    def check_args(self, args: argparse.Namespace) -> None:
        """Checks command line arguments."""
        # Does nothing by default

    @abc.abstractmethod
    def do_run(self, args: argparse.Namespace) -> None:
        """Runs the script code."""
        raise NotImplementedError

    def read_args(self) -> argparse.Namespace:
        """Reads command line arguments."""

        parser = argparse.ArgumentParser(
            description=self._desc,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)

        # Logging options
        parser.add_argument("-q", dest="quiet", action="store_true",
                            help="Set verbose level to 0.")
        parser.add_argument("--log-file", dest="log_file", required=False,
                            help="Path to a log file.")
        parser.add_argument("-v", action="count", dest="verbose", default=1,
                            help="Set verbose level.")

        # Custom options
        self.declare_args(parser)

        # Parse arguments
        args = parser.parse_args()

        # Custom check
        self.check_args(args)

        return args

    def run(self) -> None:
        """Executes script code."""

        status = 0

        try:
            # Read cmd line args
            args = self.read_args()

            # Configure logging
            configure_logging(args.verbose, args.log_file)
            logger.debug("Arguments: %s", args)

            # Run custom code
            self.do_run(args)

        except Exception as e:  # pylint: disable=broad-exception-caught
            logger.debug(traceback.format_exc())
            logger.fatal("Exception occured: %s", e)
            status = 1

        sys.exit(status)
