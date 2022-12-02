from ventil import And, Or, Not, Wire, Lamp, Xor


if __name__ == '__main__':
    lamp = Lamp()
    wire1 = Wire()
    wire2 = Wire()
    and1 = And()
    xor1 = Xor()

    # wire1.set_out(and1.in1)
    # wire2.set_out(and1.in2)
    # and1.set_out(lamp.in1)
    
    wire1.set_out(xor1.in1)
    wire2.set_out(xor1.in2)
    xor1.set_out(lamp.in1)

    for i in range(2):
        for j in range(2):
            wire1.set_signal(i)
            wire2.set_signal(j)

    # wire1.set_signal(3)
    # wire2.set_signal(2)












