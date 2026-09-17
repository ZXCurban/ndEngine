from typing import cast

import pytest

from ndengine.math.matrix import Matrix
from ndengine.math.vector import Vector


def _make_3x3() -> Matrix:
    return Matrix([Vector([1, 2, 3]), Vector([4, 5, 6]), Vector([7, 8, 9])])


def _as_lists(matrix: Matrix) -> list[list[float]]:
    column = cast(Vector, matrix[:, 0])
    row = cast(Vector, matrix[0])
    return [[cast(float, matrix[r, c]) for c in range(len(row))] for r in range(len(column))]


def test_setitem_element() -> None:
    m = Matrix([Vector([1, 2]), Vector([3, 4])])
    m[0, 0] = 10
    m[1, 1] = 40.5
    m[-1, -2] = 30
    assert _as_lists(m) == [[10, 2], [30, 40.5]]


def test_setitem_element_wrong_type_raises() -> None:
    m = Matrix([Vector([1, 2]), Vector([3, 4])])
    with pytest.raises(TypeError):
        m[0, 0] = Vector([1, 2])  # type: ignore[assignment]
    with pytest.raises(TypeError):
        m[0, 0] = "x"  # type: ignore[assignment]


def test_setitem_row_slice() -> None:
    m = _make_3x3()
    m[0, 0:2] = Vector([10, 20])
    m[1, 1:] = Vector([50, 60])
    assert _as_lists(m) == [[10, 20, 3], [4, 50, 60], [7, 8, 9]]


def test_setitem_row_slice_errors() -> None:
    m = _make_3x3()
    with pytest.raises(TypeError):
        m[0, 0:2] = Matrix([Vector([1, 2])])  # type: ignore[assignment]
    with pytest.raises(ValueError):
        m[0, 0:2] = Vector([1, 2, 3])


def test_setitem_column_slice() -> None:
    m = _make_3x3()
    m[0:2, 0] = Vector([10, 40])
    m[:, 2] = Vector([30, 60, 90])
    assert _as_lists(m) == [[10, 2, 30], [40, 5, 60], [7, 8, 90]]


def test_setitem_column_slice_errors() -> None:
    m = _make_3x3()
    with pytest.raises(TypeError):
        m[0:2, 0] = 5  # type: ignore[assignment]
    with pytest.raises(ValueError):
        m[0:2, 0] = Vector([1, 2, 3])


def test_setitem_submatrix() -> None:
    m = _make_3x3()
    m[0:2, 0:2] = Matrix([Vector([10, 20]), Vector([40, 50])])
    assert _as_lists(m) == [[10, 20, 3], [40, 50, 6], [7, 8, 9]]


def test_setitem_submatrix_errors() -> None:
    m = _make_3x3()
    with pytest.raises(TypeError):
        m[0:2, 0:2] = Vector([1, 2])  # type: ignore[assignment]
    with pytest.raises(ValueError):
        m[0:2, 0:2] = Matrix([Vector([1, 2])])
    with pytest.raises(ValueError):
        m[0:2, 0:2] = Matrix([Vector([1, 2, 3]), Vector([4, 5, 6])])


def test_setitem_row() -> None:
    m = Matrix([Vector([1, 2]), Vector([3, 4])])
    m[0] = Vector([10, 20])
    assert _as_lists(m) == [[10, 20], [3, 4]]


def test_setitem_row_copies_value() -> None:
    m = Matrix([Vector([1, 2]), Vector([3, 4])])
    v = Vector([10, 20])
    m[0] = v
    v[0] = 99
    assert m[0, 0] == 10


def test_setitem_row_errors() -> None:
    m = Matrix([Vector([1, 2]), Vector([3, 4])])
    with pytest.raises(TypeError):
        m[0] = 5  # type: ignore[assignment]
    with pytest.raises(ValueError):
        m[0] = Vector([1, 2, 3])


def test_setitem_rows_slice() -> None:
    m = _make_3x3()
    m[0:2] = Matrix([Vector([10, 20, 30]), Vector([40, 50, 60])])
    assert _as_lists(m) == [[10, 20, 30], [40, 50, 60], [7, 8, 9]]


def test_setitem_rows_slice_copies_value() -> None:
    m = _make_3x3()
    sub = Matrix([Vector([10, 20, 30])])
    m[0:1] = sub
    sub[0, 0] = 99
    assert m[0, 0] == 10


def test_setitem_rows_slice_errors() -> None:
    m = _make_3x3()
    with pytest.raises(TypeError):
        m[0:2] = Vector([1, 2, 3])  # type: ignore[assignment]
    with pytest.raises(ValueError):
        m[0:2] = Matrix([Vector([1, 2, 3])])


def test_setitem_bad_key_and_arity_raises() -> None:
    m = Matrix([Vector([1, 2])])
    with pytest.raises(IndexError):
        m[0, 0, 0] = 1  # type: ignore[index]
    with pytest.raises(TypeError):
        m["x"] = Vector([1, 2])  # type: ignore[index]
    with pytest.raises(TypeError):
        m[1.5] = Vector([1, 2])  # type: ignore[index]
    with pytest.raises(TypeError):
        m["a", "b"] = Vector([1, 2])  # type: ignore[index]
    with pytest.raises(TypeError):
        m[0, "b"] = Vector([1, 2])  # type: ignore[index]
    with pytest.raises(TypeError):
        m["a", 0] = Vector([1, 2])  # type: ignore[index]


def test_len() -> None:
    assert len(Matrix([Vector([1, 2])])) == 1
    assert len(_make_3x3()) == 3


def test_iter_yields_rows() -> None:
    m = Matrix([Vector([1, 2]), Vector([3, 4])])
    rows = list(iter(m))
    assert rows == [Vector([1, 2]), Vector([3, 4])]


def test_repr() -> None:
    m = Matrix([Vector([1, 2]), Vector([3, 4])])
    assert repr(m) == f"Matrix([\n    {Vector([1, 2])!r},\n    {Vector([3, 4])!r}\n])"


def test_eq() -> None:
    a = Matrix([Vector([1, 2]), Vector([3, 4])])
    b = Matrix([Vector([1, 2]), Vector([3, 4])])
    c = Matrix([Vector([1, 2]), Vector([3, 5])])
    assert a == b
    assert a != c
    assert a != "not a matrix"
    assert a != Matrix([Vector([1, 2])])


def test_copy_is_isolated() -> None:
    m = Matrix([Vector([1, 2]), Vector([3, 4])])
    clone = m.copy()
    assert clone == m
    clone[0, 0] = 99
    assert m[0, 0] == 1
    m[1, 1] = 99
    assert clone[1, 1] == 4
