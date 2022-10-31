from ventil import And, Or, Not, Provod, Lamp

if __name__ == '__main__':
    lamp = Lamp()
    provod1 = Provod()
    provod2 = Provod()
    and1 = And()

    provod1.set_out(and1.in1)
    provod2.set_out(and1.in2)
    and1.set_out(lamp.in1)

    # for i in range(2):
    #     for j in range(2):
    #         provod1.set_signal(i)
    #         provod2.set_signal(j)

    provod1.set_signal(3)
    provod2.set_signal(2)












