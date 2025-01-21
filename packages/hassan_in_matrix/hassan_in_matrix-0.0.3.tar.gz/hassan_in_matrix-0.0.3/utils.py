from matrix import Matrix


def input_matrix(square: bool = False) -> Matrix:
    m = []
    longestRow = 0

    print(
        "Enter a binary matrix using 0 and 1 without any delimiters, and press Enter for each row. Press another Enter when it's done."
    )

    while True:
        rowInput = input()
        if rowInput == "":
            break
        row = [bool(int(s)) for s in rowInput]
        if len(row) > longestRow:
            longestRow = len(row)
        m.append(row)

    if square:
        # Make the matrix square by filling rows with zero
        for row in m:
            if len(row) < longestRow:
                row += [False] * (longestRow - len(row))
        while len(m) < longestRow:
            m.append([False] * longestRow)

    return Matrix(m)
