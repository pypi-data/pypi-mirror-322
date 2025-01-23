# pylint: disable=missing-module-docstring
import collections.abc
import typing
from .elem_seq import ElemSeq
from .elements import Elements


class ElemSeqGen(collections.abc.Iterator[ElemSeq]):
    """A sequence generator.

    :param seq_len: The seq_len of the sequence.
    :param elements: The elements of the sequence with their weights (integer values).
        See Elements class.
    """

    def __init__(self, seq_len: int, count: int = 1,
                 elements: Elements | None = None) -> None:
        self._seq_len = seq_len
        self._count = count
        self._elements = Elements() if elements is None else elements

        self._n = 0  # Number of sequences already generated.

    @property
    def elements(self) -> Elements:
        """Returns the weights of the elements.

        :return: The defined weights.
        """
        return self._elements

    def __iter__(self) -> typing.Self:
        """Gets the iterator on the sequence.

        :return: Itself as an iterator.
        """
        return self

    def __next__(self) -> ElemSeq:
        """Generates a sequence.

        :return: A fully generated sequence.
        """
        if self._n >= self._count:
            raise StopIteration

        # Count generated sequences
        self._n += 1

        return ElemSeq(self._elements.get_rand_elem(length=self._seq_len))
