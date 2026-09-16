from typing import cast

import pytest

from ndengine.math.matrix import Matrix
from ndengine.math.vector import Vector


def _as_lists(matrix: Matrix) -> list[list[float]]:
    column = cast(Vector, matrix[:, 0])
    row = cast(Vector, matrix[0])
    return [[cast(float, matrix[r, c]) for c in range(len(row))] for r in range(len(column))]


def test_init_copies_rows() -> None:
    v1 = Vector([1, 2])
    v2 = Vector([3, 4])
    m = Matrix([v1, v2])
    v1[0] = 99
    assert m[0, 0] == 1
    assert m[1, 1] == 4


def test_init_accepts_generator() -> None:
    m = Matrix(row for row in [Vector([1, 2]), Vector([3, 4])])
    assert _as_lists(m) == [[1, 2], [3, 4]]


def test_init_empty_raises() -> None:
    with pytest.raises(ValueError):
        Matrix([])


def test_init_non_vector_row_raises() -> None:
    with pytest.raises(TypeError):
        Matrix([[1, 2]])  # type: ignore[list-item]


def test_init_ragged_rows_raises() -> None:
    with pytest.raises(ValueError):
        Matrix([Vector([1, 2]), Vector([1, 2, 3])])


def test_getitem_row_int() -> None:
    m = Matrix([Vector([1, 2]), Vector([3, 4])])
    assert m[0] == Vector([1, 2])
    assert m[1] == Vector([3, 4])
    assert m[-1] == Vector([3, 4])


def test_getitem_row_slice_returns_submatrix() -> None:
    m = Matrix([Vector([1, 2]), Vector([3, 4]), Vector([5, 6])])
    assert _as_lists(cast(Matrix, m[0:2])) == [[1, 2], [3, 4]]
    assert _as_lists(cast(Matrix, m[1:])) == [[3, 4], [5, 6]]


def test_getitem_element() -> None:
    m = Matrix([Vector([1, 2]), Vector([3, 4])])
    assert m[0, 0] == 1
    assert m[0, 1] == 2
    assert m[1, 0] == 3
    assert m[1, 1] == 4
    assert m[-1, -1] == 4


def test_getitem_row_and_column_slice_returns_coordinates() -> None:
    m = Matrix([Vector([1, 2, 3]), Vector([4, 5, 6])])
    assert m[0, 0:2] == [1, 2]
    assert m[1, 1:] == [5, 6]


def test_getitem_column_slice_per_row_returns_vector() -> None:
    m = Matrix([Vector([1, 2]), Vector([3, 4])])
    assert cast(Vector, m[:, 0]) == Vector([1, 3])
    assert cast(Vector, m[:, 1]) == Vector([2, 4])
    assert cast(Vector, m[-2:, 0]) == Vector([1, 3])


def test_getitem_submatrix() -> None:
    m = Matrix([Vector([1, 2, 3]), Vector([4, 5, 6]), Vector([7, 8, 9])])
    assert _as_lists(cast(Matrix, m[0:2, 0:2])) == [[1, 2], [4, 5]]
    assert _as_lists(cast(Matrix, m[0:2, 1:3])) == [[2, 3], [5, 6]]
    assert _as_lists(cast(Matrix, m[1:, 1:])) == [[5, 6], [8, 9]]


def test_getitem_submatrix_is_isolated() -> None:
    m = Matrix([Vector([1, 2, 3]), Vector([4, 5, 6]), Vector([7, 8, 9])])
    sub = cast(Matrix, m[0:2, 0:2])
    row = cast(Vector, m[0])
    row[0] = 99
    assert _as_lists(sub) == [[1, 2], [4, 5]]


def test_chained_indexing() -> None:
    m = Matrix([Vector([1, 2]), Vector([3, 4])])
    assert cast(Vector, m[1])[0] == 3
    assert cast(Vector, m[0])[1] == 2


def test_getitem_wrong_tuple_arity_raises() -> None:
    m = Matrix([Vector([1, 2])])
    with pytest.raises(IndexError):
        m[0, 0, 0]  # type: ignore[index]
    with pytest.raises(IndexError):
        m[(0,)]  # type: ignore[index]


def test_getitem_bad_key_raises() -> None:
    m = Matrix([Vector([1, 2])])
    with pytest.raises(TypeError):
        m["x"]  # type: ignore[index]
    with pytest.raises(TypeError):
        m["a", "b"]  # type: ignore[index]
    with pytest.raises(TypeError):
        m[1.5]  # type: ignore[index]
