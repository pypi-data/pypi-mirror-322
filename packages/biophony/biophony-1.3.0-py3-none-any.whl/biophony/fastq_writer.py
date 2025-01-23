# pylint: disable=missing-module-docstring
import typing

from .bio_read import BioRead


class FastqWriter:
    # pylint: disable=too-few-public-methods
    """FASTA file writer.

    :param output: An output stream.
    """

    def __init__(self, output: typing.TextIO) -> None:
        self._output = output

    def write_reads(self, reads: typing.Iterable[BioRead]) -> None:
        """Writes a series of reads into a FASTQ file.

        :param reads: An iterable on BioRead objects.
        """

        for read in reads:
            self.write_read(read)

    def write_read(self, read: BioRead) -> None:
        """Writes a read into a FASTQ file.

        :param read: The read object to write.
        """

        # Header
        header = f"@{read.seq.seqid}"
        if read.seq.desc != "":
            header += f" {read.seq.desc}"

        # Set lines
        read_lines = [header, str(read.seq.seq), "+", read.qual]

        # Write
        self._output.write("\n".join(read_lines) + "\n")
