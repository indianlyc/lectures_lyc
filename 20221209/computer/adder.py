from ventil import Xor, And, WireOut, Or
import numpy as np


class HalfAdder:
    """
    Полусумматор
    """
    def __init__(self):
        self._in_a = None
        self._in_b = None
        self._out_s = None  # разряд суммы
        self._out_co = None  # разряд переноса

        self._xor = Xor()
        self._and = And()
        self._wire1 = WireOut()
        self._wire2 = WireOut()

        self._xor.set_out(self._wire1.in1)
        self._and.set_out(self._wire2.in1)

    def _set_none(self):
        self._out_s = None
        self._out_co = None

    def _result(self):
        self._xor.in1(self._in_a)
        self._and.in1(self._in_a)
        self._xor.in2(self._in_b)
        self._and.in2(self._in_b)
        return self._wire1.get_signal(), self._wire2.get_signal()

    def in_a(self, value):
        """
        Установка входа _in_a
        :param value:
        :return:
        """
        self._in_a = value
        if self._in_b is not None:
            out1, out2 = self._result()
            self._out_s(out1)
            self._out_co(out2)
            self._set_none()

    def in_b(self, value):
        """
        Установка входа _in_b
        :param value:
        :return:
        """
        self._in_b = value
        if self._in_a is not None:
            out1, out2 = self._result()
            self._out_s(out1)
            self._out_co(out2)
            self._set_none()

    def set_out(self, out1, out2):
        self._out_s = out1
        self._out_co = out2


class BinaryAdder:
    """
    Сумматор
    """
    def __init__(self):
        self._in_ci = None
        self._in_a = None
        self._in_b = None
        self._out_s = None
        self._out_co = None

        self._ha1 = HalfAdder()
        self._ha2 = HalfAdder()
        self._or = Or()
        self._wire1 = WireOut()
        self._wire2 = WireOut()

        self._ha1.set_out(self._wire1.in1, self._or.in1)
        self._ha2.set_out(self._ha1.in_b, self._or.in2)
        self._or.set_out(self._wire2.in1)

    def _result(self):
        self._ha1.in_a(self._in_ci)
        self._ha2.in_a(self._in_a)
        self._ha2.in_b(self._in_b)
        return self._wire1.get_signal(), self._wire2.get_signal()

    def in_ci(self, value):
        self._in_ci = value
        if self._in_a is not None and self._in_b is not None:
            out1, out2 = self._result()
            self._out_s(out1)
            self._out_co(out2)
            self._set_none()

    def in_a(self, value):
        self._in_a= value
        if self._in_ci is not None and self._in_b is not None:
            out1, out2 = self._result()
            self._out_s(out1)
            self._out_co(out2)
            self._set_none()

    def in_b(self, value):
        self._in_b = value
        if self._in_ci is not None and self._in_a is not None:
            out1, out2 = self._result()
            self._out_s(out1)
            self._out_co(out2)
            self._set_none()

    def set_out(self, out1, out2):
        self._out_s = out1
        self._out_co = out2

    def _set_none(self):
        self._in_ci = None
        self._in_a = None
        self._in_b = None


class BinaryAdder8:
    def __init__(self):
        self._n = 8
        # входы A и B
        self._in_a = []
        self._in_b = []
        self._in_ci = None
        # сумматоры
        self._ba = []
        #  провода которые свяжут выход от сумматоров с выходами 8битного сумматора
        self._wire_out = []
        # провод от выхода для переноса
        self._wire_co = WireOut()

        self._out_s = []
        self._out_co = None


        for i in range(self._n):
            self._out_s.append(None)
            self._in_a.append(None)
            self._in_b.append(None)
            self._ba.append(BinaryAdder())
            self._wire_out.append(WireOut())

        for i in range(self._n-1):
            self._ba[i].set_out(self._wire_out[i].in1, self._ba[i+1].in_ci)

        self._ba[self._n - 1].set_out(self._wire_out[self._n - 1].in1, self._wire_co.in1)

    def _set_none(self):
        # входы A и B
        self._in_a = []
        self._in_b = []
        self._in_ci = None

    def set_out(self, out1, out2):
        self._out_s = out1
        self._out_co = out2


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