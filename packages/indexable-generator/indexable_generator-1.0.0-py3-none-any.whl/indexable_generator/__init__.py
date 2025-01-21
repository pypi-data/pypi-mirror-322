import functools
import itertools
from typing import Any, Callable, Iterator, List, Tuple, Union, _alias

__version__ = '1.0.0'


class IndexableGenerator:
    """Implement Sequence functionalities to a generator object.

    These include getitem, index and length. Values are cached as they are
    consumed from the generator.

    Examples:
        .. code-block:: python

            ig = IndexableGenerator((x for x in range(10)))
            ig[3:6]  # (3, 4, 5)

            @IndexableGenerator.cast
            def gen():
                for x in range(10):
                    yield x
            ig = gen()
            ig[3:6]  # (3, 4, 5)
    """

    cache: List[Any]
    """Holds the values already extracted from the generator."""
    it: Iterator[Any]
    """Pointer to the input generator."""

    def __init__(self, it: Iterator[Any]):
        """Default constructor.

        Args:
            it: input generator to be treated as an indexable sequence.
        """
        self.cache: List[Any] = []
        self.it: Iterator[Any] = it

    def __getitem__(self, index: Union[int, slice]) -> Union[Tuple[Any], Any]:
        """Get value(s) at input index/indices from the stream of values.

        Args:
            index: either the index of an element in the sequence, or a slice
                of element indices.

        Returns:
            Either a tuple of values or a single value at input index/indices.
        """
        head = len(self.cache)
        if isinstance(index, slice):
            start = index.start or 0
            stop = -1 if index.stop is None else index.stop
            if start < 0 or stop < 0:
                self._consume()
            elif index.stop > head:
                r = list(itertools.islice(self.it, index.stop - head))
                self.cache.extend(r)
        elif index < 0:
            if not len(self):
                return
        elif index > head - 1:
            r = list(itertools.islice(self.it, index - head + 1))
            self.cache.extend(r)
            head += len(r)
        return self.cache.__getitem__(index)

    def __iter__(self):
        return itertools.chain(self.cache, self._iter())

    def __len__(self):
        self._consume()
        return len(self.cache)

    def __next__(self):
        """Transparently delegate calls to next() to the inside generator."""
        try:
            result = next(self.it)
            self.cache.append(result)
            return result
        except StopIteration:
            return None

    def _consume(self):
        result = list(self.it)
        self.cache.extend(result)

    def _iter(self):
        for x in self.it:
            self.cache.append(x)
            yield x

    @classmethod
    def cast(cls, func: Callable) -> Callable:
        """Decorator for functions returning a generator."""
        @functools.wraps(func)
        def decorated(*args, **kwargs):
            return cls(func(*args, **kwargs))
        return decorated

    def index(self, item: Any) -> int:
        """Get the index of an item in the sequence.

        Args:
            item: object to search for.

        Returns:
            index of input item.

        Raises:
            ValueError: raised when item not found.
        """
        if item in self.cache:
            return self.cache.index(item)
        for x in self._iter():
            if x == item:
                return len(self.cache) - 1
        raise ValueError(f"{item} not in IndexableGenerator")


T_IndexableGenerator = _alias(IndexableGenerator, 1)
