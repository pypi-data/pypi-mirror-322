"""Module for FASTA Generator CLI."""
# pylint: disable=duplicate-code

import argparse
import gzip
import logging
import sys

from .cli_script import CliScript
from .bio_seq_gen import BioSeqGen
from .elements import Elements
from .fasta_writer import FastaWriter

logger = logging.getLogger("biophony")


class FastaGenScript(CliScript):
    """FASTA Generator Script class."""

    def __init__(self) -> None:
        super().__init__(desc="Generates FASTA files.")

    def declare_args(self, p: argparse.ArgumentParser) -> None:
        """Declares command line arguments."""

        p.add_argument("-n", "--length", dest="length", default=1000,
                       type=int,
                       help="The length of the generated sequence.")
        p.add_argument("--line-size", dest="line_size", default=80,
                       type=int,
                       help="Maximum number of characters on each line.")
        p.add_argument("-e", "--elements", dest="elements", default="ACTG",
                       help="The set of elements to use.")
        p.add_argument("-s", "--seqid", dest="seqid", default="chr",
                       help="SeqID.")
        p.add_argument("-H", "--header", dest="header",
                       action=argparse.BooleanOptionalAction,
                       help=("Add generation metadata in the fasta file"
                             + " header."))

        p.add_argument("-o", "--output", default="-",
                       help="Path to output file. Set to \"-\" for stdout.")
        p.add_argument("-z", "--gzip", action="store_true",
                       help="Generate gzipped output.")

    def check_args(self, args: argparse.Namespace) -> None:

        # Check output
        if args.gzip and args.output == "-":
            raise ValueError("Cannot output gzipped stream on stdout."
                             + " Please choose a valid file name.")

    def do_run(self, args: argparse.Namespace) -> None:
        """Runs FASTA Generator code."""

        gen = BioSeqGen(elements=Elements(args.elements),
                        seqlen=args.length, prefix_id=args.seqid)

        # Gzipped
        if args.gzip:
            with gzip.open(args.output, "wt", encoding="utf-8") as f:
                FastaWriter(f, seq_line_len=args.line_size,
                            header=args.header).write_seqs(gen)

        # Plain output
        else:
            # stdout
            if args.output == "-":
                FastaWriter(output=sys.stdout, seq_line_len=args.line_size,
                            header=args.header).write_seqs(gen)

            # File
            else:
                with open(args.output, "w", encoding="utf-8") as f:
                    FastaWriter(f, seq_line_len=args.line_size,
                                header=args.header).write_seqs(gen)


def fastagen_cli() -> None:
    """FASTA generation CLI.
    """

    FastaGenScript().run()
