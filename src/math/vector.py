import math

class ndVector:
    def __init__(self, coordinates):
        self.coordinates = coordinates

    def __getitem__(self, key):
        return self.coordinates[key]

    def __setitem__(self, key, value):
        self.coordinates[key] = value

    def __len__(self):
        return len(self.coordinates)

    def __add__(self, other):
        if len(self.coordinates) != len(other.coordinates):
            raise ValueError("Cannot add vectors of different dimensions")
        return ndVector([
            i[0] + i[1]
            for i in zip(self.coordinates, other.coordinates)
        ])

    def __sub__(self, other):
        if len(self.coordinates) != len(other.coordinates):
            raise ValueError("Cannot subtract vectors of different dimensions")
        return ndVector([
            i[0] - i[1]
            for i in zip(self.coordinates, other.coordinates)
        ])

    def __mul__(self, other):
        if not isinstance(other, (int, float)):
            return NotImplemented
        return ndVector([
            i * other
            for i in self.coordinates
        ])

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if not isinstance(other, (int, float)):
            return NotImplemented
        return ndVector([
            i/other
            for i in self.coordinates
        ])

    def __neg__(self):
        return ndVector([-x for x in self.coordinates])

    def length(self):
        return math.sqrt(sum(i**2 for i in self.coordinates))

    def normalize(self):
        length = self.length()

        if length == 0:
            raise ValueError("Cannot normalize zero vector")

        return self / length

    def dot(self, other):
        if len(self.coordinates) != len(other.coordinates):
            raise ValueError("Cannot calculate dot product of vectors with different dimensions")
        return sum(
            i[0] * i[1]
            for i in zip(self.coordinates, other.coordinates)
        )

    def angle_to(self, other):
        self_length = self.length()
        other_length = other.length()

        if not self_length or not other_length:
            raise ValueError("Cannot calculate angle with zero vector")

        return math.acos(
            self.dot(other) / (self_length * other_length)
        )

#a⋅b=a1​b1​+a2​b2​+a3​b3
#∣v∣=x12​+x22​+⋯+xn2​



Na = ndVector([1, 2, 3])
Nb = ndVector([10, 20, 30])

Nc = Na + Nb
Nd = Na - Nb
Nf = 5*Na
Ng = Na/2

print(Nc.coordinates)
print(Nd.coordinates)
print(Nf.coordinates)
print(Ng.coordinates)

print(Na[1])

Na[1] = 3

print(Na[1])
print(len(Na))

Nh = -Na

print(Nh.coordinates)

v = ndVector([3, 4])
n = v.normalize()

print(n.coordinates)
print(n.length())