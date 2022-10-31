class Provod:
    def __init__(self):
        self._out = None

    def set_out(self, out):
        self._out = out

    def set_signal(self, value):
        self._out(value)


class Lamp:
    def in1(self, value):
        print(int(value != 0))

class And:
    """
      | 0 1
    --------
    0 | 0 0
    1 | 0 1
    """
    def __init__(self):
        self._out = None
        self._in1 = None
        self._in2 = None

    def _result(self):
        return self._in1 & self._in2

    def _set_none(self):
        self._in1 = None
        self._in2 = None

    def in1(self, value):
        self._in1 = value
        if self._in2 is not None:
            self._out(self._result())
            self._set_none()

    def in2(self, value):
        self._in2 = value
        if self._in1 is not None:
            self._out(self._result())
            self._set_none()

    def set_out(self, out):
        self._out = out



class Or(And):
    """
      | 0 1
    --------
    0 | 0 1
    1 | 1 1
    """
    def _result(self):
        return self._in1 | self._in2


class Not:
    """
      | 0 1
    --------
      | 1 0
    """
    pass


class AndNot:
    pass


class OrNot:
    pass


class Xor:
    pass
