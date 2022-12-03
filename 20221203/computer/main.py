from ventil import And, Or, Not, WireIn, Lamp, Xor
from adder import HalfAdder, BinaryAdder

if __name__ == '__main__':
    # lamp = Lamp()
    # wire1 = WireIn()
    # wire2 = WireIn()
    # and1 = And()
    # xor1 = Xor()

    # wire1.set_out(and1.in1)
    # wire2.set_out(and1.in2)
    # and1.set_out(lamp.in1)
    
    # wire1.set_out(xor1.in1)
    # wire2.set_out(xor1.in2)
    # xor1.set_out(lamp.in1)
    #
    # for i in range(2):
    #     for j in range(2):
    #         wire1.set_signal(i)
    #         wire2.set_signal(j)

    # wire1.set_signal(3)
    # wire2.set_signal(2)
    lamp1 = Lamp("lamp1")
    lamp2 = Lamp("lamp2")
    wire1 = WireIn()
    wire2 = WireIn()
    wire3 = WireIn()

    ba = BinaryAdder()

    wire1.set_out(ba.in1)
    wire2.set_out(ba.in2)
    wire3.set_out(ba.in3)

    ba.set_out(lamp1.in1, lamp2.in1)

    for k in range(2):
        for i in range(2):
            for j in range(2):
                print(f"set signal {k} {i} {j}")
                wire1.set_signal(k)
                wire2.set_signal(i)
                wire3.set_signal(j)










