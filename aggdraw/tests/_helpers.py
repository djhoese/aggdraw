"""Shared utilities for inspecting what aggdraw actually drew."""

from PIL import Image


WHITE = (255, 255, 255)


def to_image(draw):
    """Convert a Draw surface to a PIL Image."""
    return Image.frombytes(draw.mode, draw.size, draw.tobytes())


def ink_count(im):
    """Count the pixels in an image that aren't the white background."""
    width, height = im.size
    return sum(
        1
        for y in range(height)
        for x in range(width)
        if im.getpixel((x, y)) != WHITE
    )
