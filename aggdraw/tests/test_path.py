import aggdraw
import pytest


class TestPath():

    def test_init(self):
        # Create empty path
        p = aggdraw.Path()

        # Create path with existing points
        pts = (0, 0, 10, 0, 10, 10)
        p = aggdraw.Path(pts)

    def test_coords(self):
        pts = [0, 0, 10, 0, 10, 10]
        p = aggdraw.Path(pts)
        assert p.coords() == pts

    def test_close(self):
        # NOTE: Can't actually test without drawing and checking pixels
        pts = (0, 0, 10, 0, 10, 10)
        p = aggdraw.Path(pts)
        p.close()

    def test_curveto(self):
        p = aggdraw.Path()
        p.moveto(5, 5)
        p.curveto(10, 10, 15, 0, 20, 5)
        pts = p.coords()
        # Check that bezier goes down, then up, then down
        assert pts[1] == pts[-1]
        assert pts[2] > pts[0]
        assert pts[3] > pts[1]
        assert pts[-1] > pts[-3]
        assert pts[-2] > pts[-4]
        assert pts[-1] == 5
        assert pts[-2] == 20

    def test_lineto(self):
        p = aggdraw.Path()
        p.lineto(10, 15)
        p.lineto(5, 10)
        pts = p.coords()
        assert pts == [10, 15, 5, 10]

    def test_moveto(self):
        # NOTE: lineto and moveto have same effect on p.coords() but are
        # still drawn differently
        p = aggdraw.Path()
        p.moveto(20, 20)
        assert p.coords() == [20, 20]

    def test_rcurveto(self):
        p = aggdraw.Path()
        p.moveto(5, 5)
        p.rcurveto(5, 5, 10, -5, 15, 0)
        pts = p.coords()
        # Check that bezier goes down, then up, then down
        assert pts[1] == pts[-1]
        assert pts[2] > pts[0]
        assert pts[3] > pts[1]
        assert pts[-1] > pts[-3]
        assert pts[-2] > pts[-4]
        assert pts[-1] == 5
        assert pts[-2] == 20

    def test_rlineto(self):
        p = aggdraw.Path()
        p.moveto(10, 10)
        p.rlineto(-5, 5)
        assert p.coords() == [10, 10, 5, 15]

    def test_rmoveto(self):
        p = aggdraw.Path()
        p.moveto(10, 10)
        p.rlineto(10, 10)
        p.rmoveto(-5, 5)
        p.rlineto(10, 10)
        pts = p.coords()
        assert pts == [10, 10, 20, 20, 15, 25, 25, 35]

    def test_draw(self):
        # Create a test path
        p = aggdraw.Path()
        p.moveto(10, 10)
        p.lineto(90, 10)
        p.curveto(50, 50, 60, 40, 90, 90)
        p.rlineto(-80, 0)
        p.close()
        # Draw it using the methods that draw Paths
        pen = aggdraw.Pen("black", width=1)
        draw = aggdraw.Draw("RGB", (100, 100))
        draw.line(p, pen)
        draw.polygon(p, pen)
        draw.symbol((0, 0), p, pen)
        draw.path(p, pen)
