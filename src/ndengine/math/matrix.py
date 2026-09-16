from __future__ import annotations

from collections.abc import Iterable
from typing import cast

from ndengine.math.vector import Vector

Coordinate = int | float
Row = Vector


class Matrix:
    _rows: list[Row]

    def __init__(self, rows: Iterable[Row]) -> None:
        rows = list(rows)

        if not rows:
            raise ValueError("Matrix cannot be empty")

        if not all(isinstance(row, Vector) for row in rows):
            raise TypeError("Matrix rows must be vectors")

        columns = len(rows[0])

        if not all(len(row) == columns for row in rows):
            raise ValueError("All matrix rows must have the same dimension")

        self._rows = [row.copy() for row in rows]

    def __getitem__(
        self,
        key: int | slice | tuple[int | slice, int | slice],
    ) -> Coordinate | Row | list[Coordinate] | Matrix:
        if isinstance(key, tuple):
            if len(key) != 2:
                raise IndexError("Matrix index must contain exactly two indices")

            row_key, column_key = key

            if isinstance(row_key, int) and isinstance(column_key, (int, slice)):
                return self._rows[row_key][column_key]

            if isinstance(row_key, slice) and isinstance(column_key, int):
                return Vector(cast(Coordinate, row[column_key]) for row in self._rows[row_key])

            selected_rows = self._rows[row_key]

            return Matrix(Vector(cast(list[Coordinate], row[column_key])) for row in selected_rows)

        if isinstance(key, int):
            return self._rows[key]

        if isinstance(key, slice):
            return Matrix(self._rows[key])

        raise TypeError(
            "Matrix index must be an integer, slice, or a tuple of two integers or slices"
        )

    def __setitem__(
        self,
        key: int | slice | tuple[int | slice, int | slice],
        value: Coordinate | Row | Matrix,
    ) -> None:
        pass
