import numpy as np

import mfp.util as util


class Polynomial:
    """
    Definition 2.1: a single-variable polynomial with real coefficients is a
    function f that takes a real number as input, produces a real number as
    output, and has the form

        f(x) = a_0 + a_1 * x + a_2 * x^2 + ... + a_n * x^n

        where the a_i are real numbers called the coefficients of f. The degree
        of the polynomial is the number n.
    """

    __slots__ = ["_coefficients"]

    def __init__(self, coefficients, nonzero=False):
        """
        :param coefficients: a list of real values that are the coefficients
               of the polynomial.
        """
        self._coefficients = util.trim(coefficients[:], 0)
        if len(self._coefficients) > 0:
            assert self._coefficients[-1] != 0
        if nonzero:
            assert len(self._coefficients) != 0

    def __call__(self, *args, **kwargs):
        """
        :param args: a single real value x.
        :return: the value of the Polynomial for x.
        """
        if len(kwargs) > 0:
            raise ValueError("keyword arguments aren't supported")

        if len(args) != 1:
            raise ValueError(
                "one argument is required but {} were provided".format(len(args))
            )

        x = args[0]
        sum = 0
        for i in range(len(self._coefficients)):
            if self._coefficients[i]:
                sum += self._coefficients[i] * (x ** i)

        return sum

    def __len__(self):
        """
        The length of a Polynomial is its degree.
        """
        return len(self._coefficients)

    def degree(self):
        """
        The degree of a polynomial is the highest degree of its monomials with
        non-zero coefficients.
        """
        return len(self)

    def __repr__(self):
        return "Polynomial of degree {}".format(self.degree())

    def __str__(self):
        """A string representation of the polynomial."""
        s = "f(x) = "
        alst = []

        for i in range(len(self._coefficients)):
            if not self._coefficients[i]:
                continue
            xs = ""
            a = self._coefficients[i]
            if a < 0:
                xs += " -"
            elif i > 0:
                xs += " +"

            if i > 0:
                xs += " "

            if abs(a) != 1 or i == 0:
                xs += str(abs(a))

            if i > 1:
                xs += "x^{}".format(i)
            elif i == 1:
                xs += "x"

            s += xs
        return s

    def __add__(self, other):
        return Polynomial(
            _merge_coefficients(
                self._coefficients, other._coefficients, lambda x, y: x + y
            )
        )

    def __sub__(self, other):
        return Polynomial(
            _merge_coefficients(
                self._coefficients, other._coefficients, lambda x, y: x - y
            )
        )

    def __mul__(self, other):
        coeffs = [0] * (len(self) + len(other) - 1)
        for i, a in enumerate(self._coefficients):
            for j, b in enumerate(other._coefficients):
                coeffs[i + j] += a * b

        coeffs = util.trim(coeffs)
        return Polynomial(coeffs)

    def __eq__(self, other):
        if len(self._coefficients) != len(other._coefficients):
            return False
        return all(
            [
                np.isclose(self._coefficients[i], other._coefficients[i])
                for i in range(len(self._coefficients))
            ]
        )


ZERO = Polynomial([])


def _merge_coefficients(a1, a2, op):
    max_length = max(len(a1), len(a2))
    a1 += [0] * (max_length - len(a1))
    a2 += [0] * (max_length - len(a2))

    return [op(a1[i], a2[i]) for i in range(max_length)]


def _single_term(points, i):
    p = Polynomial([1])
    xi, yi = points[i]

    for j, point in enumerate(points):
        if j == i:
            continue
        xj = point[0]
        p *= Polynomial([-xj / (xi - xj), 1.0 / (xi - xj)])

    return p * Polynomial([yi])


def interpolate(points):
    if len(points) == 0:
        raise ValueError("interpolation requires at least one point")

    xs = [point[0] for point in points]
    if len(set(xs)) < len(xs):
        raise ValueError("interpolation requires distinct x values")

    terms = [_single_term(points, i) for i in range(len(points))]
    return sum(terms, ZERO)
