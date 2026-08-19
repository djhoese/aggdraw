from PIL import Image
import pytest


def _to_image(draw):
    im = Image.frombytes(draw.mode, draw.size, draw.tobytes())
    return im


def test_module_init():
    import aggdraw
    assert hasattr(aggdraw, 'VERSION')
    assert isinstance(aggdraw.VERSION, str)
    assert hasattr(aggdraw, '__version__')
    assert isinstance(aggdraw.__version__, str)


def test_draw():
    from aggdraw import Draw
    from PIL import Image
    with pytest.raises(AttributeError) as excinfo:
        Draw("RGB")
    assert "'str' object has no attribute 'mode'" in str(excinfo.value)

    draw = Draw("RGB", (800, 600))
    assert draw.mode == 'RGB'
    assert draw.size == (800, 600)

    draw = Draw("RGB", (800, 600), "white")
    assert draw.mode == 'RGB'
    assert draw.size == (800, 600)

    im = Image.new("RGB", (600, 800))
    draw = Draw(im)
    assert draw.mode == 'RGB'
    assert draw.size == (600, 800)


def test_flush():
    from aggdraw import Draw
    from PIL import Image
    im = Image.new("RGB", (600, 800))
    draw = Draw(im)
    assert draw.flush().mode == 'RGB'


def test_pen():
    from aggdraw import Pen, Draw
    Pen("black")
    Pen("black", 1)
    Pen("black", width=1.5)
    Pen("black", 1, opacity=128)

    Pen(0)
    Pen((0,0,0))
    Pen("rgb(0,0,0)")
    Pen("gold")

    # Check that pens work as expected
    pens = {
        "black": Pen("black", 1),
        "red": Pen((255, 0, 0), 5),
        "black_50": Pen((0, 0, 0), 3, opacity=128),
        "crimson": Pen("#DC143C", 3)
    }
    surf = Draw("RGB", (50, 50), "white")
    surf.line((1, 1.5, 50, 1.5), pen=pens["black"])
    surf.line((1, 10.5, 50, 10.5), pen=pens["red"])
    surf.line((1, 20.5, 50, 20.5), pen=pens["black_50"])
    surf.line((1, 30.5, 50, 30.5), pen=pens["crimson"])
    im = _to_image(surf)
    assert im.getpixel((1, 1)) == (0, 0, 0)
    assert im.getpixel((1, 10)) == (255, 0, 0)
    assert im.getpixel((1, 20)) == (127, 127, 127)
    assert im.getpixel((1, 30)) == (220, 20, 60)
    # Check widths of lines
    assert im.getpixel((1, 8)) == (255, 0, 0)
    assert im.getpixel((1, 12)) == (255, 0, 0)
    assert im.getpixel((1, 21)) == (127, 127, 127)
    # Check outside of lines to make sure it's white
    non_line = [(0, 1), (1, 0), (1, 2), (2, 7), (20, 13)]
    for loc in non_line:
        assert im.getpixel(loc) == (255, 255, 255)


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
    im = _to_image(surf)
    assert im.getpixel((1, 1)) == (0, 0, 0)
    assert im.getpixel((51, 1)) == (255, 0, 0)
    assert im.getpixel((1, 51)) == (127, 127, 127)
    assert im.getpixel((51, 51)) == (220, 20, 60)

def test_graphics():
    from aggdraw import Draw, Pen, Brush
    draw = Draw("RGB", (500, 500))

    pen = Pen("black")
    brush = Brush("black")

    draw.line((50, 50, 100, 100), pen)

    draw.rectangle((50, 150, 100, 200), pen)
    draw.rectangle((50, 220, 100, 270), brush)
    draw.rectangle((50, 290, 100, 340), brush, pen)
    draw.rectangle((50, 360, 100, 410), pen, brush)

    draw.ellipse((120, 150, 170, 200), pen)
    draw.ellipse((120, 220, 170, 270), brush)
    draw.ellipse((120, 290, 170, 340), brush, pen)
    draw.ellipse((120, 360, 170, 410), pen, brush)

    draw.polygon((190+25, 150, 190, 200, 190+50, 200), pen)
    draw.polygon((190+25, 220, 190, 270, 190+50, 270), brush)
    draw.polygon((190+25, 290, 190, 340, 190+50, 340), brush, pen)
    draw.polygon((190+25, 360, 190, 410, 190+50, 410), pen, brush)


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


def test_graphics3():
    """See issue #22."""
    from aggdraw import Draw, Pen
    from PIL import Image
    main = Image.new('RGB', (480, 1024), 'white')
    d = Draw(main)
    p = Pen((90,) * 3, 0.5)


def test_path():
    from aggdraw import Draw, Path
    Path()
    Path([0, 0])
    Path([0, 0, 0, 0])

    p = Path()
    p.moveto(0, 0)
    p.lineto(1, 1)
    assert p.coords() == [0.0, 0.0, 1.0, 1.0]

    p.curveto(0, 0, 0, 0, 0, 0)
    p.close()
    p.coords()
    assert p.coords() == [0.0, 0.0, 1.0, 1.0, 0.125, 0.125, 0.0, 0.0]

    draw = Draw("RGB", (800, 600))
    draw.line(p)
    draw.polygon(p)
    draw.symbol((0, 0), p)
    draw.path(p)


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


def test_transform():
    from aggdraw import Draw
    draw = Draw("RGB", (500, 500))

    draw.settransform()
    draw.settransform((250, 250))
    draw.settransform((1, 0, 250, 0, 1, 250))
    draw.settransform((2.0, 0.5, 250, 0.5, 2.0, 250))
    draw.settransform()
