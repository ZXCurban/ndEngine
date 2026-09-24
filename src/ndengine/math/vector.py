from __future__ import annotations

import math
from collections.abc import Iterable, Iterator
from typing import Any, TypeGuard, overload

Coordinate = int | float


class Vector:
    _coordinates: list[Coordinate]

    def __init__(self, coordinates: Iterable[Coordinate]) -> None:
        coords = list(coordinates)

        if not coords:
            raise ValueError("Vector cannot be empty")

        if not all(self._is_num(i) for i in coords):
            raise TypeError("Vector coordinates must be int or float")

        self._coordinates = coords

    @overload
    def __getitem__(self, key: int) -> Coordinate: ...

    @overload
    def __getitem__(self, key: slice) -> list[Coordinate]: ...

    def __getitem__(self, key: int | slice) -> Coordinate | list[Coordinate]:
        return self._coordinates[key]

    def __setitem__(self, key: int | slice, value: Any) -> None:
        if isinstance(key, int):
            if not self._is_num(value):
                raise TypeError("Coordinate must be int or float")
            self._coordinates[key] = value
            return

        if isinstance(key, slice):
            values = list(value)

            indices = range(*key.indices(len(self._coordinates)))

            if len(values) != len(indices):
                raise ValueError("Cannot change vector dimension")

            if not all(self._is_num(v) for v in values):
                raise TypeError("Coordinates must be int or float")

            self._coordinates[key] = values
            return

        raise TypeError("Vector index must be an integer or slice")

    def __len__(self) -> int:
        return len(self._coordinates)

    def __add__(self, other: object) -> Vector:
        if isinstance(other, (int, float)):
            return Vector([a + other for a in self._coordinates])

        if not isinstance(other, Vector):
            return NotImplemented
        if not self._eq_len(other):
            raise ValueError("Cannot add vectors of different dimensions")
        return Vector([a + b for a, b in zip(self._coordinates, other._coordinates, strict=True)])

    def __radd__(self, other: object) -> Vector:
        return self.__add__(other)

    def __sub__(self, other: object) -> Vector:
        if isinstance(other, (int, float)):
            return Vector([a - other for a in self._coordinates])

        if not isinstance(other, Vector):
            return NotImplemented
        if not self._eq_len(other):
            raise ValueError("Cannot subtract vectors of different dimensions")
        return Vector([a - b for a, b in zip(self._coordinates, other._coordinates, strict=True)])

    def __rsub__(self, other: object) -> Vector:
        if isinstance(other, (int, float)):
            return Vector([other - a for a in self._coordinates])
        return NotImplemented

    def __mul__(self, other: object) -> Vector:
        if not self._is_num(other):
            return NotImplemented
        return Vector([i * other for i in self._coordinates])

    def __rmul__(self, other: object) -> Vector:
        return self.__mul__(other)

    def __truediv__(self, other: object) -> Vector:
        if not self._is_num(other):
            return NotImplemented
        if other == 0:
            raise ZeroDivisionError("Cannot divide vector on zero")
        return Vector([i / other for i in self._coordinates])

    def __neg__(self) -> Vector:
        return Vector([-x for x in self._coordinates])

    def __repr__(self) -> str:
        return f"Vector({self._coordinates})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vector):
            return False
        if not self._eq_len(other):
            return False
        return all(
            math.isclose(a, b, rel_tol=1e-9, abs_tol=0.0)
            for a, b in zip(self._coordinates, other._coordinates, strict=True)
        )

    def __iter__(self) -> Iterator[Coordinate]:
        return iter(self._coordinates)

    def copy(self) -> Vector:
        return Vector(list(self._coordinates))

    def _eq_len(self, other: Vector) -> bool:
        return len(self._coordinates) == len(other._coordinates)

    @staticmethod
    def _is_num(value: object) -> TypeGuard[Coordinate]:
        return isinstance(value, (int, float))

    def length(self) -> float:
        return math.sqrt(sum(i**2 for i in self._coordinates))

    def normalize(self) -> Vector:
        length = self.length()

        if length == 0:
            raise ValueError("Cannot normalize zero vector")

        return self / length

    def dot(self, other: Vector) -> float:
        if not isinstance(other, Vector):
            raise TypeError(f"Dot product requires another Vector, but got {type(other).__name__}")
        if not self._eq_len(other):
            raise ValueError("Cannot calculate dot product of vectors with different dimensions")
        return sum(a * b for a, b in zip(self._coordinates, other._coordinates, strict=True))

    def angle_to(self, other: Vector) -> float:
        if not isinstance(other, Vector):
            raise TypeError("Angle calculation requires another Vector")
        self_length = self.length()
        other_length = other.length()

        if not self_length or not other_length:
            raise ValueError("Cannot calculate angle with zero vector")

        cos_angle = max(min(self.dot(other) / (self_length * other_length), 1.0), -1.0)

        return math.acos(cos_angle)
