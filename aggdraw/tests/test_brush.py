"""Tests for the Brush class."""

from aggdraw.tests._helpers import to_image


def test_brush():
    from aggdraw import Brush, Draw
    Brush("black")
    Brush("black", opacity=128)

    Brush(0)
    Brush((0, 0, 0))
    Brush("rgb(0, 0, 0)")
    Brush("gold")

    # Check that brushes work as expected
    brushes = {
        "black": Brush("black"),
        "red": Brush((255, 0, 0)),
        "black_50": Brush((0, 0, 0), opacity=128),
        "crimson": Brush("#DC143C")
    }
    surf = Draw("RGB", (100, 100), "white")
    surf.rectangle((0, 0, 50, 50), brush=brushes["black"])
    surf.rectangle((50, 0, 100, 50), brush=brushes["red"])
    surf.rectangle((0, 50, 50, 100), brush=brushes["black_50"])
    surf.rectangle((50, 50, 100, 100), brush=brushes["crimson"])
    im = to_image(surf)
    assert im.getpixel((1, 1)) == (0, 0, 0)
    assert im.getpixel((51, 1)) == (255, 0, 0)
    assert im.getpixel((1, 51)) == (127, 127, 127)
    assert im.getpixel((51, 51)) == (220, 20, 60)
