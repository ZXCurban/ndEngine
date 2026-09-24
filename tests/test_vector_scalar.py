import pytest

from ndengine.math.vector import Vector


def test_add_scalar() -> None:
    assert Vector([1, 2]) + 10 == Vector([11, 12])
    assert Vector([1.5, -2.5]) + 0.5 == Vector([2.0, -2.0])
    assert Vector([1, 2]) + 0 == Vector([1, 2])
    assert Vector([1, 2]) + -3 == Vector([-2, -1])


def test_radd_scalar() -> None:
    assert 10 + Vector([1, 2]) == Vector([11, 12])
    assert 0.5 + Vector([1.5, -2.5]) == Vector([2.0, -2.0])
    assert -3 + Vector([1, 2]) == Vector([-2, -1])


def test_add_scalar_does_not_mutate() -> None:
    v = Vector([1, 2])
    result = v + 5
    assert v == Vector([1, 2])
    assert result == Vector([6, 7])
    result[0] = 99
    assert v == Vector([1, 2])


def test_radd_scalar_does_not_mutate() -> None:
    v = Vector([1, 2])
    result = 5 + v
    assert v == Vector([1, 2])
    assert result == Vector([6, 7])


def test_sub_scalar() -> None:
    assert Vector([3, 4]) - 1 == Vector([2, 3])
    assert Vector([1.5, -2.5]) - 0.5 == Vector([1.0, -3.0])
    assert Vector([1, 2]) - 0 == Vector([1, 2])
    assert Vector([1, 2]) - -3 == Vector([4, 5])


def test_rsub_scalar() -> None:
    assert 10 - Vector([1, 2]) == Vector([9, 8])
    assert 0.5 - Vector([1.5, -2.5]) == Vector([-1.0, 3.0])
    assert 0 - Vector([1, -2]) == Vector([-1, 2])


def test_sub_scalar_does_not_mutate() -> None:
    v = Vector([3, 4])
    result = v - 1
    assert v == Vector([3, 4])
    assert result == Vector([2, 3])

    result2 = 10 - v
    assert v == Vector([3, 4])
    assert result2 == Vector([7, 6])


def test_add_sub_scalar_non_numeric_raises() -> None:
    with pytest.raises(TypeError):
        Vector([1, 2]) + "a"
    with pytest.raises(TypeError):
        "a" + Vector([1, 2])
    with pytest.raises(TypeError):
        Vector([1, 2]) - "a"
    with pytest.raises(TypeError):
        "a" - Vector([1, 2])
    with pytest.raises(TypeError):
        Vector([1, 2]) + [3, 4]
    with pytest.raises(TypeError):
        [3, 4] + Vector([1, 2])
    with pytest.raises(TypeError):
        Vector([1, 2]) - [1, 2]
    with pytest.raises(TypeError):
        Vector([1, 2]) + None  # type: ignore[operator]
