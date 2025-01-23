# pylint: disable=missing-module-docstring
from .bio_seq import BioSeq


class BioRead:
    """Describes a read sequence: ID, description, sequence, quality.
    
    The class contains a BioSeq object that contains the sequence, its ID and
    its description.
    It also contains the quality as a string.

    :param seq: A BioSeq object.
    :param qual: The quality of the sequence.
    """

    def __init__(self, seq: BioSeq, qual: str) -> None:
        self._seq = seq
        self._qual = qual

    @property
    def seq(self) -> BioSeq:
        """The sequence as a BioSeq object."""
        return self._seq

    @property
    def qual(self) -> str:
        """The quality of the sequence."""
        return self._qual
