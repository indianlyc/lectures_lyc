from ventil import Xor, And, WireOut, Or
import numpy as np


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
        if self._in2 is not None and self._in3 is not None:
            out1, out2 = self._result()
            self._out1(out1)
            self._out2(out2)
            self._set_none()

    def in2(self, value):
        self._in2 = value
        if self._in1 is not None and self._in3 is not None:
            out1, out2 = self._result()
            self._out1(out1)
            self._out2(out2)
            self._set_none()

    def in3(self, value):
        self._in3 = value
        if self._in1 is not None and self._in2 is not None:
            out1, out2 = self._result()
            self._out1(out1)
            self._out2(out2)
            self._set_none()

    def set_out(self, out1, out2):
        self._out1 = out1
        self._out2 = out2


class BinaryAdder8:
    def __init__(self):
        self._n = 8
        # входы A и B
        self._a_in = []
        self._b_in = []
        self._ci_in = None
        # сумматоры
        self._ba = []
        #  провода к которым подсоединим лампочки
        self._wire_out = []
        # провод от выхода для переноса
        self._wire_move = WireOut()

        self._s_out = []
        self._co_out = None


        for i in range(self._n):
            self._s_out.append(None)
            self._a_in.append(None)
            self._b_in.append(None)
            self._ba.append(BinaryAdder())
            self._wire_out.append(WireOut())

        for i in range(self._n-1):
            self._ba[i].set_out(self._wire_out[i].in1, self._ba[i+1].in3)

        self._ba[self._n - 1].set_out(self._wire_out[self._n - 1].in1, self._wire_move.in1)

    def __getattr__(self, attr):
        # attr = "in_a0"
        # i = 0, s = a
        i = int(attr[4:])
        s = attr[3]
        def wrap(self, value):
            return self._in_summary(i, value)
        return wrap

    def _in_summary(self, i, value):
        self._a[i] = value
        if np.all(self._a) is not None:
            outs = self._result()
            for i, el in enumerate(outs):
                self._out[i](el)
            self._set_none()