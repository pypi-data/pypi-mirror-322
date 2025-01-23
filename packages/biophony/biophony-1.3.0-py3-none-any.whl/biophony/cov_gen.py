"""Coverage generation."""
import logging
import random
import typing

logger = logging.getLogger("biophony")


class CovItem:
    """A coverage item corresponding to a line in a BED file.

    :param chrom: The chromosome.
    :param pos:   The position.
    :param depth: The coverage depth.
    """

    def __init__(self, chrom: str, pos: int, depth: int) -> None:
        self._chrom = chrom
        self._pos = pos
        self._depth = depth

    def __repr__(self) -> str:
        return f"chr{self._chrom},pos={self._pos},depth={self._depth}"

    def to_bed_line(self) -> str:
        """Exports this item as BED file line.
        """
        return f"chr{self._chrom}\t{self._pos}\t{self._depth}"


# pylint: disable-next=too-many-instance-attributes
class CovGen:
    """Generator of coverage items to write into a coverage BED file.

    :param chrom: Chromosome identifier.
    :param min_pos: Minimum position where coverage starts.
    :param max_pos: Maximum position where coverage ends.
    :param min_depth: Minimum depth of coverage allowed.
    :param max_depth: Maximum depth of coverage allowed.
    :param depth_offset: Position where coverage depth starts being generated.
    :param depth_change_rate: Probability of depth fluctuation at each position.
    """

    # pylint: disable=too-many-arguments, too-many-positional-arguments
    def __init__(self, chrom: str = "1", min_pos: int = 0, max_pos: int = 10000,
                 min_depth: int = 0, max_depth: int = 0, depth_offset: int = 0,
                 depth_change_rate: float = 0.0) -> None:
        self._chrom = chrom
        self._min_pos = min_pos
        self._max_pos = max_pos
        self._min_depth = min_depth
        self._max_depth = max_depth
        self._depth_offset = depth_offset
        self._depth_change_rate = depth_change_rate

        self._pos = -1
        self._depth: typing.Optional[int] = None

    def __iter__(self) -> "CovGen":
        """Gets the iterator on the coverage items.

        :return: Itself as an iterator.
        """
        return self

    def __next__(self) -> CovItem:
        """Generates a coverage item.
        
        :return: A coverage item.
        """

        # Increase position
        if self._pos < 0:
            self._pos = self._min_pos
        else:
            self._pos += 1

        # Done
        if self._pos > self._max_pos:
            raise StopIteration

        # Update depth
        if self._depth is None:
            if self._pos >= self._depth_offset:
                self._depth = random.randint(self._min_depth, self._max_depth)
        elif self._depth_change_rate > 0.0:
            if random.random() <= self._depth_change_rate:
                self._depth += -1 if random.randint(0, 1) == 0 else +1
                self._depth = min(self._depth, self._max_depth)
                self._depth = max(self._depth, self._min_depth)

        # Generate a new item
        item = CovItem(self._chrom, self._pos,
                       0 if self._depth is None else self._depth)

        return item
