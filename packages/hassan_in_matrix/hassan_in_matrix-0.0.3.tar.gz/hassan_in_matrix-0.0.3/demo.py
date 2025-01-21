from utils import input_matrix

print("DM v1.0.0 by Hassan Heydari Nasab")
print("License: WTFPL")
print("Matrix is a class in matrix.py file and contains useful methods.")
print("You can find the test cases in test.py or choose a demo:")

while True:
    print("1. multiply matrices")
    print("2. Rn matrix")
    print("3. join matrices")
    print("4. meet matrices")
    print("5. is reflexive")
    print("6. is symmetric")
    print("7. is antisymmetric")
    print("8. is transitive")
    print("9. is equivalent")
    print("10. reflexive closure")
    print("11. symmetric closure")
    print("12. transitive closure")
    print("13. transitive closure using Floyd-Warshall's algorithm")

    demo = input("Enter a number [1-13]: ")

    print("\n" * 200)

    if demo == "1":
        m1 = input_matrix()
        m2 = input_matrix()
        print("\nResult:")
        print(m1 * m2)
    elif demo == "2":
        m = input_matrix()
        p = int(input("Enter the power: "))
        print("\nResult:")
        print(m**p)
    elif demo == "3":
        m1 = input_matrix()
        m2 = input_matrix()
        print(m1)
        print(m2)
        print("\nResult:")
        print(m1 | m2)
    elif demo == "4":
        m1 = input_matrix()
        m2 = input_matrix()
        print("\nResult:")
        print(m1 & m2)
    elif demo == "5":
        m = input_matrix()
        print("\nResult:")
        print(m.is_reflexive())
    elif demo == "6":
        m = input_matrix()
        print("\nResult:")
        print(m.is_symmetric())
    elif demo == "7":
        m = input_matrix()
        print("\nResult:")
        print(m.is_antisymmetric())
    elif demo == "8":
        m = input_matrix()
        print("\nResult:")
        print(m.is_transitive())
    elif demo == "9":
        m = input_matrix()
        print("\nResult:")
        print(m.is_equivalent())
    elif demo == "10":
        m = input_matrix()
        print("\nResult:")
        print(m.reflexive_closure())
    elif demo == "11":
        m = input_matrix()
        print("\nResult:")
        print(m.symmetric_closure())
    elif demo == "12":
        m = input_matrix()
        print("\nResult:")
        print(m.transitive_closure())
    elif demo == "13":
        m = input_matrix()
        print("\nResult:")
        print(m.transitive_closure_using_warshall_alg())
    else:
        print("Are we done? Bye!")
        exit(0)

    input("\nDone! Press Enter to continue...")
    print("\n" * 200)
