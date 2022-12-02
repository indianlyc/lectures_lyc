class Wire:
    def __init__(self):
        self._out = ()

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
    def __init__(self):
        self._out = None
        self._in1 = None

    def _result(self):
        return ~self._in1

    def _set_none(self):
        self._in1 = None

    def in1(self, value):
        self._in1 = value
        self._out(self._result())
        self._set_none()

    def set_out(self, out):
        self._out = out


class AndNot(And):
    """
      | 0 1
    --------
    0 | 1 1
    1 | 1 0
    """
    def _result(self):
        return ~(self._in1 & self._in2)


class OrNot(And):
    """
      | 0 1
    --------
    0 | 1 0
    1 | 0 0
    """
    def _result(self):
        return ~(self._in1 | self._in2)


class Xor(And):
    """
      | 0 1
    --------
    0 | 0 1
    1 | 1 0
    """
    def __init__(self):
        super().__init__()

        self._or = Or()
        self._and_not = AndNot()

        self._and = And()
        self._or.set_out(self._and.in1)
        self._and_not.set_out(self._and.in2)
    
    def _result(self):
        self._or.in1(self._in1)
        self._and_not.in1(self._in1)
        self._or.in2(self._in2)
        self._and_not.in2(self._in2)
        return self._and._result()
        

        
    
