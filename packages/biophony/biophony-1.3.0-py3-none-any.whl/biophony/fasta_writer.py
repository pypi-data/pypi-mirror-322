# pylint: disable=missing-module-docstring
import datetime
import typing
from .bio_seq import BioSeq


class FastaWriter:
    # pylint: disable=too-few-public-methods
    """FASTA file writer.

    :param output: An output stream.
    :param seq_line_len: The max length of sequence lines.
    :param header: If enabled, writes a header at start of file (i.e.: lines
            starting with a semicolon).
    """

    def __init__(self, output: typing.TextIO,
                 seq_line_len: int = 80, header: bool = True) -> None:
        self._output = output
        self._seq_line_len = seq_line_len
        if header:
            self._write_header()

    def _write_header(self) -> None:
        date = datetime.datetime.now()
        print(f"; Generated on {date} by biophony package.",
              file=self._output)

    def write_seqs(self, seqs: typing.Iterator[BioSeq]) -> None:
        """Write a series of sequences."""
        for seq in seqs:
            self.write_bio_seq(seq)

    def write_bio_seq(self, seq: BioSeq) -> None:
        """Writes a sequence to the file.

        :param seq: The sequence to write.
        """
        # ID/Description line
        s = f">{seq.seqid}"
        if seq.desc != "":
            s += f" {seq.desc}"
        fasta = [s]

        # Sequence lines
        i = 0
        while i < len(seq.seq):
            end = min(i + self._seq_line_len, len(seq.seq))
            fasta.append(seq.seq[i:end])
            i = end

        # Write
        self._output.write("\n".join(fasta) + "\n")
