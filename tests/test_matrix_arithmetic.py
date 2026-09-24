from typing import cast

import pytest

from ndengine.math.matrix import Matrix
from ndengine.math.vector import Vector


def _make_2x2() -> Matrix:
    return Matrix([Vector([1, 2]), Vector([3, 4])])


def _as_lists(matrix: Matrix) -> list[list[float]]:
    column = cast(Vector, matrix[:, 0])
    row = cast(Vector, matrix[0])
    return [[cast(float, matrix[r, c]) for c in range(len(row))] for r in range(len(column))]


def test_neg() -> None:
    assert _as_lists(-_make_2x2()) == [[-1, -2], [-3, -4]]
    assert _as_lists(-Matrix([Vector([1.5, -2.0])])) == [[-1.5, 2.0]]
    negated = -_make_2x2()
    assert -negated == _make_2x2()


def test_neg_does_not_mutate() -> None:
    m = _make_2x2()
    result = -m
    assert _as_lists(m) == [[1, 2], [3, 4]]
    assert _as_lists(result) == [[-1, -2], [-3, -4]]
    result[0, 0] = 99
    assert m[0, 0] == 1


def test_add_matrix() -> None:
    a = _make_2x2()
    b = Matrix([Vector([10, 20]), Vector([30, 40])])
    assert _as_lists(a + b) == [[11, 22], [33, 44]]


def test_add_scalar() -> None:
    assert _as_lists(_make_2x2() + 10) == [[11, 12], [13, 14]]
    assert _as_lists(_make_2x2() + 0.5) == [[1.5, 2.5], [3.5, 4.5]]
    assert _as_lists(_make_2x2() + -1) == [[0, 1], [2, 3]]
    assert _as_lists(_make_2x2() + 0) == [[1, 2], [3, 4]]


def test_radd_scalar() -> None:
    assert _as_lists(10 + _make_2x2()) == [[11, 12], [13, 14]]
    assert _as_lists(0.5 + _make_2x2()) == [[1.5, 2.5], [3.5, 4.5]]


def test_add_does_not_mutate() -> None:
    a = _make_2x2()
    b = Matrix([Vector([10, 20]), Vector([30, 40])])
    result = a + b
    assert _as_lists(a) == [[1, 2], [3, 4]]
    assert _as_lists(b) == [[10, 20], [30, 40]]
    result[0, 0] = 99
    assert a[0, 0] == 1
    assert b[0, 0] == 10


def test_add_scalar_does_not_mutate() -> None:
    m = _make_2x2()
    result = m + 5
    assert _as_lists(m) == [[1, 2], [3, 4]]
    assert _as_lists(result) == [[6, 7], [8, 9]]


def test_add_dimension_mismatch_raises() -> None:
    a = _make_2x2()
    b = Matrix([Vector([1, 2, 3]), Vector([4, 5, 6])])
    c = Matrix([Vector([1, 2])])
    with pytest.raises(ValueError):
        a + b
    with pytest.raises(ValueError):
        a + c


def test_add_bad_type_raises() -> None:
    m = _make_2x2()
    with pytest.raises(TypeError):
        m + "a"
    with pytest.raises(TypeError):
        m + [1, 2]
    with pytest.raises(TypeError):
        "a" + m
    with pytest.raises(TypeError):
        m + None  # type: ignore[operator]


def test_sub_matrix() -> None:
    a = Matrix([Vector([10, 20]), Vector([30, 40])])
    b = _make_2x2()
    assert _as_lists(a - b) == [[9, 18], [27, 36]]


def test_sub_scalar() -> None:
    assert _as_lists(_make_2x2() - 1) == [[0, 1], [2, 3]]
    assert _as_lists(_make_2x2() - 0.5) == [[0.5, 1.5], [2.5, 3.5]]
    assert _as_lists(_make_2x2() - -1) == [[2, 3], [4, 5]]


def test_rsub_scalar() -> None:
    assert _as_lists(10 - _make_2x2()) == [[9, 8], [7, 6]]
    assert _as_lists(0 - _make_2x2()) == [[-1, -2], [-3, -4]]
    assert _as_lists(0.5 - Matrix([Vector([1.5, 2.5])])) == [[-1.0, -2.0]]


def test_sub_does_not_mutate() -> None:
    a = Matrix([Vector([10, 20]), Vector([30, 40])])
    b = _make_2x2()
    result = a - b
    assert _as_lists(result) == [[9, 18], [27, 36]]
    assert _as_lists(a) == [[10, 20], [30, 40]]
    assert _as_lists(b) == [[1, 2], [3, 4]]

    m = _make_2x2()
    rsub = 10 - m
    assert _as_lists(m) == [[1, 2], [3, 4]]
    assert _as_lists(rsub) == [[9, 8], [7, 6]]


def test_sub_dimension_mismatch_raises() -> None:
    a = _make_2x2()
    b = Matrix([Vector([1, 2, 3]), Vector([4, 5, 6])])
    with pytest.raises(ValueError):
        a - b


def test_sub_bad_type_raises() -> None:
    m = _make_2x2()
    with pytest.raises(TypeError):
        m - "a"
    with pytest.raises(TypeError):
        m - [1, 2]


def test_mul_scalar() -> None:
    assert _as_lists(_make_2x2() * 2) == [[2, 4], [6, 8]]
    assert _as_lists(_make_2x2() * 0) == [[0, 0], [0, 0]]
    assert _as_lists(_make_2x2() * -1) == [[-1, -2], [-3, -4]]
    assert _as_lists(_make_2x2() * 0.5) == [[0.5, 1.0], [1.5, 2.0]]


def test_rmul_scalar() -> None:
    assert _as_lists(2 * _make_2x2()) == [[2, 4], [6, 8]]
    assert _as_lists(0.5 * _make_2x2()) == [[0.5, 1.0], [1.5, 2.0]]
    assert _as_lists(-1 * _make_2x2()) == [[-1, -2], [-3, -4]]


def test_mul_does_not_mutate() -> None:
    m = _make_2x2()
    result = m * 3
    assert _as_lists(m) == [[1, 2], [3, 4]]
    assert _as_lists(result) == [[3, 6], [9, 12]]
    result[0, 0] = 99
    assert m[0, 0] == 1


def test_mul_bad_type_raises() -> None:
    m = _make_2x2()
    with pytest.raises(TypeError):
        m * "a"
    with pytest.raises(TypeError):
        m * Vector([1, 2])
    with pytest.raises(TypeError):
        m * m
    with pytest.raises(TypeError):
        "a" * m
