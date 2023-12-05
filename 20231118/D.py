with open("input.txt") as f_in:
    n = int(f_in.readline())


with open("output.txt", "w") as f_out:

    print_array = [0]*2*n
    a = ["("]*n
    b = []

    def f(i):
        # print("array",i, print_array, "a", a, "b", b)
        if len(a):
            print_array[i] = a.pop()
            b.append(")")
            f(i+1)
            # print("f",i)
            print_array[i] = 0
            b.pop()
            a.append("(")
        # print("-array",i, print_array, "a", a, "b", b)
        if len(b):
            print_array[i] = b.pop()
            f(i+1)
            # print("-f",i)
            print_array[i] = 0
            b.append(")")
        else:
            if i == len(print_array):
                # print("print", "".join(print_array))
                f_out.write("".join(print_array)+"\n")


    f(0)