# pylint: disable=missing-module-docstring
import argparse
import logging
import re
import typing

from .cli_script import CliScript
from .cov_gen import CovGen

logger = logging.getLogger("biophony")


def parse_range(s: str) -> typing.Tuple[int, int]:
    # pylint: disable=missing-function-docstring

    m = re.search(r"^(?P<begin>[0-9]+)(-(?P<end>[0-9]+))?$", s)
    if m:
        begin = int(m.group("begin"))
        if m.group("end") is None:
            end = begin
        else:
            end = int(m.group("end"))
    else:
        raise ValueError(f"Wrong range \"{s}\"pos.")

    return begin, end


class CovGenScript(CliScript):
    """Coverage Script class."""

    def __init__(self) -> None:
        super().__init__(desc="Generates BED files.")

    def declare_args(self, p: argparse.ArgumentParser) -> None:
        """Declares command line arguments."""

        p.add_argument("-c", "--chrom", dest="chrom", type=str, default="1",
                       help="The chromosome for which to generate a BED file.")
        p.add_argument("-p", "--pos", dest="pos", type=str, default="0-10000",
                       help=("The positions to generate."
                             + " Either a single value or a range begin-end"
                             + ", where end is included."))
        p.add_argument("-d", "--depth", dest="depth", type=str, default="0",
                       help=("The depth to generate. A single value or a range"
                             + " start-stop, stop included."))
        p.add_argument("-r", "--depth-change-rate", dest="depth_change_rate",
                       type=float, default=0.0,
                       help="Set depth change rate.")
        p.add_argument("-s", "--depth-start", dest="depth_start", type=int,
                       default="0",
                       help=("The starting position from which depth will be"
                             + " generated. Any position before this one will"
                             + " get a depth of 0."))

    def do_run(self, args: argparse.Namespace) -> None:
        """Runs Coverage Generator code."""

        pos_range = parse_range(args.pos)
        depth_range = parse_range(args.depth)
        gen = CovGen(
            chrom=args.chrom,
            min_pos=pos_range[0],
            max_pos=pos_range[1],
            min_depth=depth_range[0],
            max_depth=depth_range[1],
            depth_offset=args.depth_start,
            depth_change_rate=args.depth_change_rate
        )
        for item in gen:
            print(item.to_bed_line())


def covgen_cli() -> None:
    """Coverage generation CLI.
    """

    CovGenScript().run()
