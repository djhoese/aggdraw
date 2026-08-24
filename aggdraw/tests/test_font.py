"""Tests for the Font class."""

import glob
import os

import pytest

import aggdraw
from aggdraw.tests._helpers import WHITE, ink_count, to_image


FONT_DIRS = [
    "/usr/share/fonts",  # linux
    "/usr/local/share/fonts",  # linux
    "/System/Library/Fonts",  # macos
    "/Library/Fonts",  # macos
    os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts"),  # windows
]


def _find_font():
    """Return the path of any TrueType font on this machine, or None.

    aggdraw ships no font of its own and Pillow's default font is not a file
    on disk, so there is nothing portable to point Font() at.
    """
    for directory in FONT_DIRS:
        matches = sorted(glob.glob(os.path.join(directory, "**", "*.ttf"), recursive=True))
        if matches:
            return matches[0]
    return None


def _font_or_skip(color="black", size=12):
    """Build a Font, skipping the test if fonts or FreeType are unavailable."""
    if not hasattr(aggdraw.Draw("RGB", (1, 1), "white")._draw, "text"):
        pytest.skip("built without FreeType, so there is no text renderer")
    path = _find_font()
    if path is None:
        pytest.skip("no TrueType font found on this machine")
    return aggdraw.Font(color, path, size)


def test_font_metrics_are_str():
    """family and style are str, not bytes.

    They used to be built with PyBytes_FromString, a leftover from Python 2
    where that produced a str.
    """
    # these attributes are only exposed on the underlying C object
    cfont = _font_or_skip("black")._font

    assert isinstance(cfont.family, str)
    assert isinstance(cfont.style, str)
    assert cfont.family
    assert isinstance(cfont.ascent, float)
    assert isinstance(cfont.descent, float)


def test_font_draws_text():
    """Text actually puts ink on the surface, in the requested color."""
    font = _font_or_skip("red", 24)

    surf = aggdraw.Draw("RGB", (200, 60), "white")
    width, height = surf.textsize("Hello", font)
    assert width > 0
    assert height > 0

    surf.text((5, 5), "Hello", font)
    im = to_image(surf)
    assert ink_count(im) > 0
    # every inked pixel is some blend of red over white
    for x in range(im.width):
        for y in range(im.height):
            r, g, b = im.getpixel((x, y))
            if (r, g, b) != WHITE:
                assert g == b
                assert r >= g
