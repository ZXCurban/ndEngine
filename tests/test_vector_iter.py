from ndengine.math.vector import Vector


def test_iter_yields_coordinates() -> None:
    v = Vector([1, 2.5, -3])
    assert list(v) == [1, 2.5, -3]
    assert list(iter(v)) == [1, 2.5, -3]


def test_iter_supports_unpacking_and_zip() -> None:
    a, b, c = Vector([1, 2, 3])
    assert (a, b, c) == (1, 2, 3)
    assert list(zip([0, 1], Vector([10, 20]), strict=True)) == [(0, 10), (1, 20)]
