import pytest

from mfp import poly


def test_poly_1():
    p = poly.Polynomial([1])
    assert p(0) == 1


def test_add_polys():
    f = poly.Polynomial([1, 2])
    g = poly.Polynomial([0, 1])
    h = f + g
    assert h(0) == 1
    assert h(1) == 4
    assert h(5) == 16


def test_sub_polys():
    f = poly.Polynomial([1, 2])
    g = poly.Polynomial([0, 1])
    h = f - g
    assert h(0) == 1
    assert h(1) == 2
    assert h(5) == 6


def test_interpolate():
    interpolations = [[(1, 1)], [(1, 1), (2, 0)], [(1, 1), (2, 4), (7, 9)]]
    expected = [
        poly.Polynomial([1.0]),
        poly.Polynomial([2.0, -1.0]),
        poly.Polynomial([-2.6666666, 3.999999, -0.333333]),
    ]
    polys = [poly.interpolate(points) for points in interpolations]
    assert all([polys[i] == expected[i] for i in range(len(polys))])
