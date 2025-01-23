"""Module for generating sequences nad their variants into a FASTA file."""

import argparse
import logging
import sys

from .bio_seq_var_gen import BioSeqVarGen
from .bio_seq_gen import BioSeqGen
from .cli_script import CliScript
from .fasta_writer import FastaWriter
from .variant_maker import VariantMaker

logger = logging.getLogger("biophony")


class FastaVarGenScript(CliScript):
    """FASTA file generator for generating sequences with their variants."""

    def __init__(self) -> None:
        super().__init__(desc=("Generates sequences and their variants as"
                               + " FASTA files."))

    def declare_args(self, p: argparse.ArgumentParser) -> None:
        """Declares command line arguments."""

        p.add_argument("--seq-length", dest="seq_len", default=60,
                       type=int,
                       help="The length of the sequences to generate.")
        p.add_argument("--nb-seq", dest="nb_seq", default=5, type=int,
                       help="The number of sequences to generate.")
        p.add_argument("--nb-var", dest="nb_var", default=1, type=int,
                       help=("The number of variants to generate for each"
                             + " sequence."))
        p.add_argument("-m", "--mut-rate", "--snp-rate", dest="mut_rate",
                       type=float, default=0.0,
                       help="The probability of mutation of one base.")
        p.add_argument("-i", "--ins-rate", dest="ins_rate",
                       type=float, default=0.0,
                       help="The probability of insertion at one base.")
        p.add_argument("-d", "--del-rate", dest="del_rate",
                       type=float, default=0.0,
                       help="The probability of deletion of one base.")

    def do_run(self, args: argparse.Namespace) -> None:
        """Runs FASTA Variants Generator code."""

        writer = FastaWriter(output=sys.stdout, seq_line_len=80)

        var_maker = VariantMaker(ins_rate=args.ins_rate,
                                 del_rate=args.del_rate,
                                 mut_rate=args.mut_rate)

        seq_gen = BioSeqGen(seqlen=args.seq_len, count=args.nb_seq,
                            prefix_id="seq")
        for seq in seq_gen:
            writer.write_bio_seq(seq)
            var_gen = BioSeqVarGen(seq.seq, var_maker=var_maker,
                                   count=args.nb_var)
            for var in var_gen:
                writer.write_bio_seq(var)


def fastavargen_cli() -> None:
    """FASTA Variant generation CLI.
    """

    FastaVarGenScript().run()
