from unittest import TestCase
from adder import HalfAdder, BinaryAdder, BinaryAdder8
from ventil import WireIn, WireOut

class TestHalfAdder(TestCase):
    def setUp(self) -> None:
        self.ha = HalfAdder()
        self.wire1_in = WireIn()
        self.wire2_in = WireIn()
        self.wire1_out = WireOut()
        self.wire2_out = WireOut()
        self.ha.set_out(self.wire1_out.in1, self.wire2_out.in1)
        self.wire1_in.set_out(self.ha.in_a)
        self.wire2_in.set_out(self.ha.in_b)
    def test_0_0(self) -> None:
        self.wire1_in.set_signal(0)
        self.wire2_in.set_signal(0)
        a1,a2 = self.wire1_out.get_signal(), self.wire2_out.get_signal()
        self.assertEqual((0,0), (a1, a2))

    def test_0_1(self) -> None:
        self.wire1_in.set_signal(0)
        self.wire2_in.set_signal(1)
        a1,a2 = self.wire1_out.get_signal(), self.wire2_out.get_signal()
        self.assertEqual((1,0), (a1, a2))

    def test_1_0(self) -> None:
        self.wire1_in.set_signal(1)
        self.wire2_in.set_signal(0)
        a1,a2 = self.wire1_out.get_signal(), self.wire2_out.get_signal()
        self.assertEqual((1,0), (a1, a2))

    def test_1_1(self) -> None:
        self.wire1_in.set_signal(1)
        self.wire2_in.set_signal(1)
        a1,a2 = self.wire1_out.get_signal(), self.wire2_out.get_signal()
        self.assertEqual((0,1), (a1, a2))


class TestBinaryAdder(TestCase):
    def setUp(self) -> None:
        self.ba = BinaryAdder()
        self.wire1_in = WireIn()
        self.wire2_in = WireIn()
        self.wire3_in = WireIn()
        self.wire1_out = WireOut()
        self.wire2_out = WireOut()
        self.ba.set_out(
            self.wire1_out.in1,
            self.wire2_out.in1,
        )
        self.wire1_in.set_out(self.ba.in_ci)
        self.wire2_in.set_out(self.ba.in_a)
        self.wire3_in.set_out(self.ba.in_b)

    def test_0_0_0(self) -> None:
        self.wire1_in.set_signal(0)
        self.wire2_in.set_signal(0)
        self.wire3_in.set_signal(0)
        a1,a2 = self.wire1_out.get_signal(), self.wire2_out.get_signal()
        self.assertEqual((0,0), (a1, a2))

    def test_0_0_1(self) -> None:
        self.wire1_in.set_signal(0)
        self.wire2_in.set_signal(0)
        self.wire3_in.set_signal(1)
        a1,a2 = self.wire1_out.get_signal(), self.wire2_out.get_signal()
        self.assertEqual((1,0), (a1, a2))

    def test_0_1_0(self) -> None:
        self.wire1_in.set_signal(0)
        self.wire2_in.set_signal(1)
        self.wire3_in.set_signal(0)
        a1,a2 = self.wire1_out.get_signal(), self.wire2_out.get_signal()
        self.assertEqual((1,0), (a1, a2))

    def test_0_1_1(self) -> None:
        self.wire1_in.set_signal(0)
        self.wire2_in.set_signal(1)
        self.wire3_in.set_signal(1)
        a1,a2 = self.wire1_out.get_signal(), self.wire2_out.get_signal()
        self.assertEqual((0,1), (a1, a2))

    def test_1_0_0(self) -> None:
        self.wire1_in.set_signal(1)
        self.wire2_in.set_signal(0)
        self.wire3_in.set_signal(0)
        a1,a2 = self.wire1_out.get_signal(), self.wire2_out.get_signal()
        self.assertEqual((1,0), (a1, a2))

    def test_1_0_1(self) -> None:
        self.wire1_in.set_signal(1)
        self.wire2_in.set_signal(0)
        self.wire3_in.set_signal(1)
        a1,a2 = self.wire1_out.get_signal(), self.wire2_out.get_signal()
        self.assertEqual((0,1), (a1, a2))

    def test_1_1_0(self) -> None:
        self.wire1_in.set_signal(1)
        self.wire2_in.set_signal(1)
        self.wire3_in.set_signal(0)
        a1,a2 = self.wire1_out.get_signal(), self.wire2_out.get_signal()
        self.assertEqual((0, 1), (a1, a2))

    def test_1_1_1(self) -> None:
        self.wire1_in.set_signal(1)
        self.wire2_in.set_signal(1)
        self.wire3_in.set_signal(1)
        a1,a2 = self.wire1_out.get_signal(), self.wire2_out.get_signal()
        self.assertEqual((1,1), (a1, a2))


class TestBinaryAdder8(TestCase):
    def setUp(self) -> None:
        self.ba8 = BinaryAdder8()
        self.wire_out_s = []
        for i in range(8):
            self.wire_out_s.append(WireOut())
        self.wire_out_co = WireOut()

        self.ba8.set_out(self.wire_out_co.in1,
                         *[el.in1 for el in self.wire_out_s])

        def get_res():
            res = []
            res.append(self.wire_out_co.get_signal())
            res2 = []
            for i in range(8):
                res2.append(self.wire_out_s[i].get_signal())
            res.extend(reversed(res2))
            return res
        self.get_res = get_res

    def test_0000000_00000000_0(self) -> None:
        self.ba8.in_a([0,0,0,0,0,0,0,0])
        self.ba8.in_b([0,0,0,0,0,0,0,0])
        self.ba8.in_ci(0)
        res = self.get_res()
        self.assertEqual([0,0,0,0,0,0,0,0,0], res)

    def test_0000001_00000001_0(self) -> None:
        self.ba8.in_a([0,0,0,0,0,0,0,1])
        self.ba8.in_b([0,0,0,0,0,0,0,1])
        self.ba8.in_ci(0)
        res = self.get_res()
        self.assertEqual([0,0,0,0,0,0,0,1,0], res)

    def test_1000001_10000001_0(self) -> None:
        self.ba8.in_a([1,0,0,0,0,0,0,1])
        self.ba8.in_b([1,0,0,0,0,0,0,1])
        self.ba8.in_ci(0)
        res = self.get_res()
        self.assertEqual([1,0,0,0,0,0,0,1,0], res)