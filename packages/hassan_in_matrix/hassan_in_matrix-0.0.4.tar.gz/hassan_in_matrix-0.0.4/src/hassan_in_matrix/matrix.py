class Matrix:
    def __init__(self, matrix: list[list[bool]]):
        if len(matrix) != 0:
            cols = len(matrix[0])
            for i in range(len(matrix)):
                if len(matrix[i]) != cols:
                    raise ValueError("Malformed matrix")
        self.m = matrix  # matrix entries
        self.r = len(matrix)  # number of rows
        self.c = 0 if self.r == 0 else len(matrix[0])  # number of columns

    def clone(self):
        return Matrix([[*r] for r in self.m])

    @classmethod
    def Zero(cls, r: int, c: int):
        return Matrix([[False] * c for _ in range(r)])

    @classmethod
    def Identity(cls, n: int):
        result: Matrix = Matrix.Zero(n, n)
        for i in range(n):
            result.m[i][i] = True
        return result

    def __repr__(self):
        result = ""
        for i in range(self.r):
            for j in range(self.c):
                result += "1" if self.m[i][j] else "0"
            result += "\n"
        return result

    def __mul__(self, other):
        if isinstance(other, bool):
            result: Matrix = Matrix(self.m)
            for i in range(len(self.m)):
                for j in range(len(self.m[0])):
                    result.m[i][j] = result.m[i][j] and other
            return result

        elif isinstance(other, Matrix):
            if self.c != other.r:
                raise ArithmeticError(
                    "Can't multiply Matrix with incompatible dimensions"
                )
            result: Matrix = Matrix.Zero(self.r, self.c)
            for i in range(self.r):
                for j in range(other.c):
                    sum = False
                    for element_index in range(self.c):
                        sum = sum or (
                            self.m[i][element_index] and other.m[j][element_index]
                        )
                    result.m[i][j] = sum
            return result
        else:
            raise ArithmeticError(
                "Can't multiply Matrix with object of type " + type(other).__name__
            )

    def __pow__(self, power: int):
        if power < 1:
            raise ArithmeticError("Can't raise a matrix to a non-positive power.")
        result = self
        for _ in range(power - 1):
            result = result.__mul__(self)
        return result
        # TODO: cache

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Matrix):
            if self.r != other.r or self.c != other.c:
                return False
            for i in range(self.r):
                for j in range(self.c):
                    if self.m[i][j] != other.m[i][j]:
                        return False
            return True
        else:
            raise ArithmeticError(
                "Can't compare Matrix with object of type " + type(other).__name__
            )

    def transposed(self):
        result: Matrix = Matrix.Zero(self.r, self.c)
        for i in range(self.r):
            for j in range(self.c):
                result.m[j][i] = self.m[i][j]
        return result

    def __and__(self, other: object):
        if isinstance(other, Matrix):
            if self.r != other.r or self.c != other.c:
                raise ArithmeticError(
                    "Can't meet with a matrix with incompatible dimensions"
                )
            result: Matrix = Matrix.Zero(self.r, self.c)
            for i in range(self.r):
                for j in range(self.c):
                    result.m[i][j] = self.m[i][j] and other.m[i][j]
            return result
        else:
            raise ArithmeticError(
                "Can't meet to object of type " + type(other).__name__
            )

    def __or__(self, other: object):
        if isinstance(other, Matrix):
            if self.r != other.r or self.c != other.c:
                raise ArithmeticError(
                    "Can't join with a matrix with incompatible dimensions"
                )
            result: Matrix = Matrix.Zero(self.r, self.c)
            for i in range(self.r):
                for j in range(self.c):
                    result.m[i][j] = self.m[i][j] or other.m[i][j]
            return result
        else:
            raise ArithmeticError(
                "Can't join to object of type " + type(other).__name__
            )

    def is_reflexive(self) -> bool:
        if self.r != self.c:
            return False

        for i in range(len(self.m)):
            if not self.m[i][i]:
                return False
        return True

    def is_symmetric(self) -> bool:
        """
        Another method to check whether a matrix is symmetric could be
        calculating the transposed matrix (which is O(n2)) then check
        if both are equal (another O(n2)).
        """
        if self.r != self.c:
            return False
        for i in range(len(self.m)):
            for j in range(len(self.m)):
                if self.m[i][j] != self.m[j][i]:
                    return False
        return True

    def is_antisymmetric(self) -> bool:
        """
        Another method to check whether a matrix is anti-symmetric could be
        calculating the transposed matrix (which is O(n2)) and then check
        if meet of the original matrix and the transposed one is less than
        or equal to I (another O(n2)).
        """
        if self.r != self.c:
            return False
        for i in range(len(self.m)):
            for j in range(len(self.m)):
                if self.m[i][j] and self.m[j][i] and i != j:
                    return False
        return True

    def is_transitive(self) -> bool:
        """
        Another method to check whether a matrix is transitive could be
        calculating the product of the matrix and itself (which is O(n3)) and then check
        if it's less than or equal to the original matrix (O(n2)).
        """
        if self.r != self.c:
            return False
        for i in range(len(self.m)):
            for j in range(len(self.m)):
                for k in range(len(self.m)):
                    if self.m[i][j] and self.m[j][k] and not self.m[i][k]:
                        return False
        return True

    def is_equivalent(self) -> bool:
        return self.is_reflexive() and self.is_symmetric() and self.is_transitive()

    def reflexive_closure(self):
        if self.c != self.r:
            raise ArithmeticError(
                "Can't calculate the reflexive closure for non-square matrix."
            )
        identity = Matrix.Identity(self.r)
        return self | identity

    def symmetric_closure(self):
        if self.c != self.r:
            raise ArithmeticError(
                "Can't calculate the symmetric closure for non-square matrix."
            )
        return self | self.transposed()

    def transitive_closure(self):
        if self.c != self.r:
            raise ArithmeticError(
                "Can't calculate the transitive closure for non-square matrix."
            )
        result = self
        for i in range(2, self.r + 1):
            result = result | self.__pow__(i)
        return result

    def transitive_closure_using_warshall_alg(self):
        if self.c != self.r:
            raise ArithmeticError(
                "Can't calculate the transitive closure for non-square matrix."
            )
        w = self.clone()
        for n in range(0, self.r):
            p = []
            q = []

            """
            for ri in range(self.r):
                if w.m[ri][n]:
                    p.append(ri)
            for ci in range(self.c):
                if w.m[n][ci]:
                    q.append(ci)

            since we ensured that the matrix is square:
            """

            for i in range(self.r):
                if w.m[i][n]:
                    p.append(i)
                if w.m[n][i]:
                    q.append(i)

            entries_to_be_one = [(pi, qi) for pi in p for qi in q]
            for entry in entries_to_be_one:
                w.m[entry[0]][entry[1]] = True
        return w
