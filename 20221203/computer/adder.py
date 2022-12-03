from ventil import Xor, And, WireOut, Or


class HalfAdder(And):
    def __init__(self):
        self._in1 = None
        self._in2 = None
        self._out1 = None
        self._out2 = None

        self._xor = Xor()
        self._and = And()
        self._wire1 = WireOut()
        self._wire2 = WireOut()

        self._xor.set_out(self._wire1.in1)
        self._and.set_out(self._wire2.in1)

    def _result(self):
        self._xor.in1(self._in1)
        self._and.in1(self._in1)
        self._xor.in2(self._in2)
        self._and.in2(self._in2)
        return self._wire1.get_signal(), self._wire2.get_signal()

    def in1(self, value):
        self._in1 = value
        if self._in2 is not None:
            out1, out2 = self._result()
            self._out1(out1)
            self._out2(out2)
            self._set_none()

    def in2(self, value):
        self._in2 = value
        if self._in1 is not None:
            out1, out2 = self._result()
            self._out1(out1)
            self._out2(out2)
            self._set_none()

    def set_out(self, out1, out2):
        self._out1 = out1
        self._out2 = out2


class BinaryAdder:
    def __init__(self):
        self._in1 = None
        self._in2 = None
        self._in3 = None
        self._out1 = None
        self._out2 = None

        self._ha1 = HalfAdder()
        self._ha2 = HalfAdder()
        self._or = Or()
        self._wire1 = WireOut()
        self._wire2 = WireOut()

        self._ha1.set_out(self._wire1._in1, self._or._in1)
        self._ha2.set_out(self._ha1._in2, self._or._in2)
        self._or.set_out(self._wire2.in1)

    def _result(self):
        self._ha1.in1(self._in1)
        self._ha2.in1(self._in2)
        self._ha2.in2(self._in3)
        return self._wire1.get_signal(), self._wire2.get_signal()

    def in1(self, value):
        self._in1 = value
        if self._in2 is not None:
            out1, out2 = self._result()
            self._out1(out1)
            self._out2(out2)
            self._set_none()

    def in2(self, value):
        self._in2 = value
        if self._in1 is not None:
            out1, out2 = self._result()
            self._out1(out1)
            self._out2(out2)
            self._set_none()

    def set_out(self, out1, out2):
        self._out1 = out1
        self._out2 = out2
