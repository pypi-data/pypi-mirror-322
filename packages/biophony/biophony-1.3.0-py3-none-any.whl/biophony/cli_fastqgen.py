"""Module for FASTQ Generator CLI."""
# pylint: disable=duplicate-code

import argparse
import gzip
import logging
import sys

from .cli_script import CliScript
from .bio_read_gen import BioReadGen
from .elements import Elements
from .fastq_writer import FastqWriter

logger = logging.getLogger("biophony")


class FastqGenScript(CliScript):
    """FASTQ Generator Script class."""

    def __init__(self) -> None:
        super().__init__(desc="Generates FASTQ files.")

    def declare_args(self, p: argparse.ArgumentParser) -> None:
        """Declares command line arguments."""

        p.add_argument("-c", "--count", dest="count", default=100, type=int,
                       help="The number of reads to generate.")
        p.add_argument("-n", "--length", dest="length", default=80, type=int,
                       help=("The length of the generated sequence in the"
                             + " reads."))
        p.add_argument("-e", "--elements", dest="elements", default="ACTG",
                       help="The set of elements to use.")
        p.add_argument("-Q", "--quality", dest="quality", default="!-~",
                       help=("The range of quality characters to use, as"
                             + "<first_char>-<last_char>."))
        p.add_argument("-r", "--readid", dest="readid", default="read",
                       help="THe prefix used to generated read IDs.")

        p.add_argument("-o", "--output", default="-",
                       help="Path to output file. Set to \"-\" for stdout.")
        p.add_argument("-z", "--gzip", action="store_true",
                       help="Generate gzipped output.")

    def check_args(self, args: argparse.Namespace) -> None:

        # Check output
        if args.gzip and args.output == "-":
            raise ValueError("Cannot output gzipped stream on stdout."
                             + " Please choose a valid file name.")

        # Parse quality range
        if len(args.quality) != 3 or args.quality[1] != "-":
            raise ValueError("The quality range must respect the format "
                             + "<first_char>-<last_char>.")
        if args.quality[0] > args.quality[2]:
            raise ValueError("In quality range, first character is greater"
                             + " than last character.")
        args.quality_range = (args.quality[0], args.quality[2])

    def do_run(self, args: argparse.Namespace) -> None:
        """Runs FASTA Generator code."""

        gen = BioReadGen(elements=Elements(args.elements),
                         quality=args.quality_range,
                         seqlen=args.length,
                         prefix_id=args.readid,
                         count=args.count)

        # Gzipped
        if args.gzip:
            with gzip.open(args.output, "wt", encoding="utf-8") as f:
                FastqWriter(f).write_reads(gen)

        # Plain output
        else:
            # stdout
            if args.output == "-":
                FastqWriter(output=sys.stdout).write_reads(gen)

            # File
            else:
                with open(args.output, "w", encoding="utf-8") as f:
                    FastqWriter(f).write_reads(gen)


def fastqgen_cli() -> None:
    """FASTQ generation CLI.
    """

    FastqGenScript().run()
