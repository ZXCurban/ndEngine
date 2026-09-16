import math

import pytest

from ndengine.math.vector import Vector


def test_init_with_list() -> None:
    v = Vector([1, 2.5, -3])
    assert len(v) == 3
    assert v[0] == 1
    assert v[1] == 2.5
    assert v[2] == -3


def test_init_with_tuple_and_other_iterable() -> None:
    assert Vector((1, 2)) == Vector([1, 2])
    assert Vector(range(3)) == Vector([0, 1, 2])
    assert Vector(x for x in [1, 2]) == Vector([1, 2])


def test_init_empty_raises() -> None:
    with pytest.raises(ValueError):
        Vector([])


def test_init_non_numeric_raises() -> None:
    with pytest.raises(TypeError):
        Vector([1, "a"])  # type: ignore[list-item]
    with pytest.raises(TypeError):
        Vector([None])  # type: ignore[list-item]
    with pytest.raises(TypeError):
        Vector([1, [2]])  # type: ignore[list-item]


def test_getitem() -> None:
    v = Vector([10, 20, 30])
    assert v[0] == 10
    assert v[-1] == 30
    assert v[0:2] == [10, 20]


def test_len() -> None:
    assert len(Vector([1])) == 1
    assert len(Vector([1, 2, 3, 4])) == 4


def test_setitem_by_index() -> None:
    v = Vector([1, 2, 3])
    v[0] = 10
    v[-1] = 30.5
    assert v == Vector([10, 2, 30.5])


def test_setitem_by_index_non_numeric_raises() -> None:
    v = Vector([1, 2, 3])
    with pytest.raises(TypeError):
        v[0] = "a"


def test_setitem_by_slice() -> None:
    v = Vector([1, 2, 3, 4])
    v[1:3] = [20, 30]
    assert v == Vector([1, 20, 30, 4])


def test_setitem_by_slice_wrong_size_raises() -> None:
    v = Vector([1, 2, 3])
    with pytest.raises(ValueError):
        v[0:2] = [1, 2, 3]


def test_setitem_by_slice_non_numeric_raises() -> None:
    v = Vector([1, 2, 3])
    with pytest.raises(TypeError):
        v[0:2] = ["a", "b"]


def test_setitem_bad_key_raises() -> None:
    v = Vector([1, 2, 3])
    with pytest.raises(TypeError):
        v["a"] = 1  # type: ignore[index]


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        ([1, 2], [3, 4], [4, 6]),
        ([0, 0], [0, 0], [0, 0]),
        ([-1, 5.5], [1, -0.5], [0, 5.0]),
        ([1, 2, 3], [-1, -2, -3], [0, 0, 0]),
    ],
)
def test_add(a: list[float], b: list[float], expected: list[float]) -> None:
    assert Vector(a) + Vector(b) == Vector(expected)


def test_add_different_dimensions_raises() -> None:
    with pytest.raises(ValueError):
        Vector([1, 2]) + Vector([1, 2, 3])


def test_add_non_vector_raises() -> None:
    with pytest.raises(TypeError):
        Vector([1, 2]) + [3, 4]
    with pytest.raises(TypeError):
        Vector([1, 2]) + 1


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        ([3, 4], [1, 2], [2, 2]),
        ([0, 0], [1, 1], [-1, -1]),
        ([1.5, 2.5], [0.5, 0.5], [1.0, 2.0]),
    ],
)
def test_sub(a: list[float], b: list[float], expected: list[float]) -> None:
    assert Vector(a) - Vector(b) == Vector(expected)


def test_sub_different_dimensions_raises() -> None:
    with pytest.raises(ValueError):
        Vector([1, 2]) - Vector([1])


def test_sub_non_vector_raises() -> None:
    with pytest.raises(TypeError):
        Vector([1, 2]) - [1, 2]


@pytest.mark.parametrize(
    ("coords", "scalar", "expected"),
    [
        ([1, 2, 3], 2, [2, 4, 6]),
        ([1, -2], -1, [-1, 2]),
        ([1.5, 2.5], 0, [0, 0]),
        ([1, 2], 0.5, [0.5, 1.0]),
    ],
)
def test_mul(coords: list[float], scalar: float, expected: list[float]) -> None:
    assert Vector(coords) * scalar == Vector(expected)
    assert scalar * Vector(coords) == Vector(expected)


def test_mul_non_numeric_raises() -> None:
    with pytest.raises(TypeError):
        Vector([1, 2]) * Vector([1, 2])
    with pytest.raises(TypeError):
        Vector([1, 2]) * "a"


@pytest.mark.parametrize(
    ("coords", "scalar", "expected"),
    [
        ([2, 4], 2, [1.0, 2.0]),
        ([1, -2], -1, [-1.0, 2.0]),
        ([1, 2], 0.5, [2.0, 4.0]),
    ],
)
def test_truediv(coords: list[float], scalar: float, expected: list[float]) -> None:
    assert Vector(coords) / scalar == Vector(expected)


def test_truediv_by_zero_raises() -> None:
    with pytest.raises(ZeroDivisionError):
        Vector([1, 2]) / 0


def test_truediv_non_numeric_raises() -> None:
    with pytest.raises(TypeError):
        Vector([1, 2]) / Vector([1, 2])
    with pytest.raises(TypeError):
        Vector([1, 2]) / "a"


def test_neg() -> None:
    assert -Vector([1, -2, 3]) == Vector([-1, 2, -3])
    assert -Vector([0, 0]) == Vector([0, 0])


def test_repr() -> None:
    assert repr(Vector([1, 2])) == "Vector([1, 2])"


def test_eq() -> None:
    assert Vector([1, 2]) == Vector([1, 2])
    assert Vector([1.0, 2.0]) == Vector([1, 2])
    # сравнение float с допуском
    assert Vector([0.1 + 0.2]) == Vector([0.3])
    assert (Vector([1, 2]) == Vector([1, 3])) is False
    assert (Vector([1, 2]) == Vector([1, 2, 3])) is False
    assert (Vector([1, 2]) == [1, 2]) is False
    assert (Vector([1, 2]) == "Vector([1, 2])") is False


def test_copy() -> None:
    v = Vector([1, 2, 3])
    c = v.copy()
    assert c == v
    assert c is not v
    c[0] = 99
    assert v[0] == 1


@pytest.mark.parametrize(
    ("coords", "expected"),
    [
        ([3, 4], 5.0),
        ([1, 0], 1.0),
        ([0, 0], 0.0),
        ([1, 2, 2], 3.0),
        ([-3, -4], 5.0),
    ],
)
def test_length(coords: list[float], expected: float) -> None:
    assert Vector(coords).length() == pytest.approx(expected)


def test_normalize() -> None:
    v = Vector([3, 4]).normalize()
    assert v.length() == pytest.approx(1.0)
    assert v == Vector([0.6, 0.8])

    v2 = Vector([0, 5]).normalize()
    assert v2 == Vector([0, 1])


def test_normalize_zero_vector_raises() -> None:
    with pytest.raises(ValueError):
        Vector([0, 0]).normalize()
    with pytest.raises(ValueError):
        Vector([0, 0, 0]).normalize()


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        ([1, 2], [3, 4], 11),
        ([1, 0], [0, 1], 0),
        ([-1, 1], [1, 1], 0),
        ([2, 3, 4], [5, 6, 7], 56),
    ],
)
def test_dot(a: list[float], b: list[float], expected: float) -> None:
    assert Vector(a).dot(Vector(b)) == pytest.approx(expected)


def test_dot_different_dimensions_raises() -> None:
    with pytest.raises(ValueError):
        Vector([1, 2]).dot(Vector([1, 2, 3]))


def test_dot_non_vector_raises() -> None:
    with pytest.raises(TypeError):
        Vector([1, 2]).dot([1, 2])  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        Vector([1, 2]).dot(5)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        ([1, 0], [1, 0], 0.0),
        ([1, 0], [0, 1], math.pi / 2),
        ([1, 0], [-1, 0], math.pi),
        ([1, 1], [1, 0], math.pi / 4),
    ],
)
def test_angle_to(a: list[float], b: list[float], expected: float) -> None:
    assert Vector(a).angle_to(Vector(b)) == pytest.approx(expected)


def test_angle_to_with_zero_vector_raises() -> None:
    with pytest.raises(ValueError):
        Vector([0, 0]).angle_to(Vector([1, 0]))
    with pytest.raises(ValueError):
        Vector([1, 0]).angle_to(Vector([0, 0]))


def test_angle_to_non_vector_raises() -> None:
    with pytest.raises(TypeError):
        Vector([1, 0]).angle_to([1, 0])  # type: ignore[arg-type]
