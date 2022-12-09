from unittest import TestCase
from adder import HalfAdder, BinaryAdder
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