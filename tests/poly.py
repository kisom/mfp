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
