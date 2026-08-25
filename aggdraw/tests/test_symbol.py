"""Tests for the Symbol class."""


def test_symbol():
    from aggdraw import Symbol

    Symbol("M0,0L0,0L0,0L0,0Z")
    Symbol("M0,0L0,0,0,0,0,0Z", 10)
    Symbol("M0,0C0,0,0,0,0,0Z")
    Symbol("M0,0S0,0,0,0,0,0Z")

    Symbol("m0,0l0,0l0,0l0,0z")
    Symbol("m0,0l0,0,0,0,0,0z", 10)
    Symbol("m0,0c0,0,0,0,0,0z")
    Symbol("m0,0s0,0,0,0,0,0z")


def test_graphics2():
    """See issue #14."""
    from aggdraw import Draw, Symbol, Pen
    from PIL import Image
    import numpy as np

    symbol = Symbol("M400 200 L400 400")
    pen = Pen("red")
    image = Image.fromarray(np.zeros((800, 600, 3), dtype=np.uint8), mode="RGB")
    canvas = Draw(image)
    canvas.symbol((0, 0), symbol, pen)
    canvas.flush()
    assert np.asarray(image).sum() == 50800


def test_invalid_symbol_does_not_leak():
    """A rejected path descriptor must release the half-built object.

    The parser's error paths used to be marked "FIXME: cleanup" and returned
    without freeing the object or its agg::path_storage.
    """
    import sys

    import pytest

    from aggdraw import Symbol

    if not sys.getallocatedblocks():
        pytest.skip("needs pymalloc to count allocated blocks")

    def build():
        # plain try/except, not pytest.raises: ExceptionInfo objects accumulate
        # and would swamp the measurement.
        try:
            Symbol("Q not a valid path")
        except ValueError:
            return
        raise AssertionError("expected ValueError")

    for _ in range(200):  # let any one-time caches settle
        build()

    before = sys.getallocatedblocks()
    for _ in range(2000):
        build()
    growth = sys.getallocatedblocks() - before

    assert growth < 100, f"failed Symbol() leaked {growth} blocks over 2000 calls"
