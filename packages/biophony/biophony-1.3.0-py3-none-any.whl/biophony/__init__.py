"""Gene files random generation.
"""
from .bio_read import BioRead
from .bio_read_gen import BioReadGen
from .bio_seq import BioSeq
from .bio_seq_gen import BioSeqGen
from .bio_seq_var_gen import BioSeqVarGen
from .elements import Elements
from .elem_seq import ElemSeq
from .elem_seq_gen import ElemSeqGen
from .elem_seq_var_gen import ElemSeqVarGen
from .fasta_writer import FastaWriter
from .fastq_writer import FastqWriter
from .variant_maker import VariantMaker
from .cov_gen import CovGen, CovItem
from .mutsim import MutSim, MutSimParams, DEFAULT_RATE, DEFAULT_SAMPLE

from .cli_fastavargen import fastavargen_cli
from .cli_fastagen import fastagen_cli
from .cli_fastqgen import fastqgen_cli
from .cli_gencov import covgen_cli
from .cli_genvcf import vcfgen_cli

__all__ = [
    "BioRead", "BioReadGen", "BioSeq", "BioSeqGen", "BioSeqVarGen",
    "Elements", "ElemSeq", "ElemSeqGen", "ElemSeqVarGen", "FastaWriter",
    "FastqWriter", "VariantMaker", "CovGen", "CovItem", "MutSim", "MutSimParams",
    "DEFAULT_RATE", "DEFAULT_SAMPLE"
]
