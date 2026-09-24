from __future__ import annotations

from collections.abc import Iterable, Iterator
from typing import overload

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

    @overload
    def __getitem__(self, key: int) -> Row: ...

    @overload
    def __getitem__(self, key: slice) -> Matrix: ...

    @overload
    def __getitem__(self, key: tuple[int, int]) -> Coordinate: ...

    @overload
    def __getitem__(
        self,
        key: tuple[int, slice],
    ) -> Coordinate | list[Coordinate]: ...

    @overload
    def __getitem__(self, key: tuple[slice, int]) -> Row: ...

    @overload
    def __getitem__(self, key: tuple[slice, slice]) -> Matrix: ...

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
                return Vector(row[column_key] for row in self._rows[row_key])

            selected_rows = self._rows[row_key]

            return Matrix(Vector(row[column_key]) for row in selected_rows)

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

        if isinstance(key, tuple):
            if len(key) != 2:
                raise IndexError("Matrix index must contain exactly two indices")

            row_key, column_key = key

            # matrix[row, column] = coordinate
            if isinstance(row_key, int) and isinstance(column_key, int):
                if not isinstance(value, (int, float)):
                    raise TypeError("Matrix element must be assigned a coordinate")

                self._rows[row_key][column_key] = value
                return

            # matrix[row, column_slice] = vector
            if isinstance(row_key, int) and isinstance(column_key, slice):
                if not isinstance(value, Vector):
                    raise TypeError("Matrix row slice must be assigned a vector")

                indices = range(*column_key.indices(len(self._rows[row_key])))

                if len(value) != len(indices):
                    raise ValueError(
                        "Assigned vector must have the same length as the selected columns"
                    )

                for column, coordinate in zip(indices, value, strict=True):
                    self._rows[row_key][column] = coordinate

                return

            # matrix[row_slice, column] = vector
            if isinstance(row_key, slice) and isinstance(column_key, int):
                rows = range(*row_key.indices(len(self)))

                if not isinstance(value, Vector):
                    raise TypeError("Matrix column slice must be assigned a vector")

                if len(value) != len(rows):
                    raise ValueError(
                        "Assigned vector must have the same length as the selected rows"
                    )

                for row, coordinate in zip(rows, value, strict=True):
                    self._rows[row][column_key] = coordinate

                return

            # matrix[row_slice, column_slice] = matrix
            if not isinstance(row_key, slice) or not isinstance(column_key, slice):
                raise TypeError(
                    "Matrix index must be an integer, slice, or a tuple of two integers or slices"
                )

            if not isinstance(value, Matrix):
                raise TypeError("Matrix slice must be assigned a matrix")

            rows = range(*row_key.indices(len(self)))
            columns = range(*column_key.indices(len(self._rows[0])))

            if len(value) != len(rows):
                raise ValueError(
                    "Assigned matrix must have the same number of rows as the selected slice"
                )

            if len(value[0]) != len(columns):
                raise ValueError(
                    "Assigned matrix must have the same number of columns as the selected slice"
                )

            for target_row, source_row in zip(rows, value, strict=True):
                for target_column, coordinate in zip(
                    columns,
                    source_row,
                    strict=True,
                ):
                    self._rows[target_row][target_column] = coordinate

            return

        # matrix[row] = vector
        if isinstance(key, int):
            if not isinstance(value, Vector):
                raise TypeError("Matrix row must be assigned a vector")

            if len(value) != len(self._rows[key]):
                raise ValueError("Assigned vector must have the same dimension as the matrix row")

            self._rows[key] = value.copy()
            return

        # matrix[row_slice] = matrix
        if isinstance(key, slice):
            if not isinstance(value, Matrix):
                raise TypeError("Matrix slice must be assigned a matrix")

            rows = range(*key.indices(len(self)))

            if len(value) != len(rows):
                raise ValueError(
                    "Assigned matrix must have the same number of rows as the selected slice"
                )

            for target_row, source_row in zip(rows, value, strict=True):
                self._rows[target_row] = source_row.copy()

            return

        raise TypeError(
            "Matrix index must be an integer, slice, or a tuple of two integers or slices"
        )

    def __len__(self) -> int:
        return len(self._rows)

    def __iter__(self) -> Iterator[Vector]:
        return iter(self._rows)

    def __repr__(self) -> str:
        rows_str = ",\n".join(f"    {row!r}" for row in self._rows)
        return f"Matrix([\n{rows_str}\n])"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Matrix):
            return False
        return len(self) == len(other) and all(a == b for a, b in zip(self, other, strict=True))

    def __neg__(self) -> Matrix:
        return Matrix(row * -1 for row in self._rows)

    def __add__(self, other: object) -> Matrix:
        if not isinstance(other, (Matrix, int, float)):
            return NotImplemented

        if isinstance(other, (int, float)):
            return Matrix(row + other for row in self._rows)

        if len(self) != len(other) or len(self._rows[0]) != len(other._rows[0]):
            raise ValueError("Cannot add matrices of different dimensions")

        return Matrix(
            left_row + right_row
            for left_row, right_row in zip(self._rows, other._rows, strict=True)
        )

    def __radd__(self, other: object) -> Matrix:
        return self.__add__(other)

    def __sub__(self, other: object) -> Matrix:
        if not isinstance(other, (Matrix, int, float)):
            return NotImplemented

        if isinstance(other, (int, float)):
            return Matrix(row - other for row in self._rows)

        if len(self) != len(other) or len(self._rows[0]) != len(other._rows[0]):
            raise ValueError("Cannot sub matrices of different dimensions")

        return Matrix(
            left_row - right_row
            for left_row, right_row in zip(self._rows, other._rows, strict=True)
        )

    def __rsub__(self, other: object) -> Matrix:
        if isinstance(other, (int, float)):
            return Matrix(other - row for row in self._rows)
        return NotImplemented

    def __mul__(self, other: object) -> Matrix:
        if not isinstance(other, (int, float)):
            return NotImplemented

        return Matrix(row * other for row in self._rows)

    def __rmul__(self, other: object) -> Matrix:
        return self.__mul__(other)

    def copy(self) -> Matrix:
        return Matrix([row.copy() for row in self])
