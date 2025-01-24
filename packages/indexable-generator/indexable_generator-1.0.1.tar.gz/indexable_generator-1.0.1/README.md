# IndexableGenerator

Implement Sequence functionalities to python Generators.

These include getitem, index and length. Values are cached as they are consumed
from the generator.

## Examples:

    @IndexableGenerator.cast
    def gen():
        for x in range(10):
            yield x

    ig = gen()
    ig[3:6]  # (3, 4, 5)

    ig = IndexableGenerator((x for x in range(10)))
    ig[3:6]  # (3, 4, 5)
