import sys

d = {
    "10": "Загрузить",
    "11": "Сохранить",
    "20": "Сложить",
    "21": "Вычесть",
    "22": "Сложить с переносом",
    "23": "Вычесть с заимстованием",
    "30": "Перейти",
    "31": "Перейти если ноль",
    "32": "Перейти если перенос",
    "33": "Перейти если не ноль",
    "34": "Перейти если не перенос",
    "40": "Сдвиг влево",
    "41": "Сдвиг вправо",
    "50": "not",
    "51": "and",
    "52": "or",
    "53": "xor",
    "ff": "Остановить",
}
class Computer:
    def __init__(self, memory_size=65536):
        self._index_use = set()
        self.mem = [0] * memory_size
        self.comment = [""] * memory_size
        self.binmem = [""] * memory_size
        self.__a = 0  # аккумулятор (защелка)
        self.__sub = 0  # признак вычитания
        self.p = 0  # выход для переноса
        self.transfer = 0  # складывать с переносом или вычитать с заимствованием
        self.is_sum = False

    @property
    def a(self):
        # аккумулятор (защелка)
        return self.__a

    @a.setter
    def a(self, value):
        if self.transfer:
            if self.__sub:
                value -= self.p
            else:
                value += self.p
            self.transfer = 0
        # print(value)
        # print(value & int("100000000", 2))
        # print(((value & int("100000000", 2)) ^ self.__sub) >> 8)
        if self.is_sum or self.__sub:
            self.p = ((value & int("100000000", 2)) ^ self.__sub) >> 8
            self.is_sum = False
        self.__a = value & int("11111111", 2)
        self.__sub = 0

    @a.deleter
    def a(self, value):
        del self.__a

    def _add_index_use(self, a:list):
        for el in a:
            self._index_use.add(el)

    def _do_command(self):
        addr = self.mem[self.i+1] * 256 + self.mem[self.i+2]
        self._add_index_use([self.i, self.i+1, self.i+2, addr])
        return addr

    def _load(self):
        addr = self._do_command()
        self.a = self.mem[addr]
        self.i += 2

    def _save(self):
        addr = self._do_command()
        self.mem[addr] = self.a
        self.i += 2

    def _add(self):
        self.is_sum = True
        addr = self._do_command()
        self.a += self.mem[addr]
        self.i += 2

    def _add_with_transfer(self):
        self.transfer = 1
        self._add()

    def _sub(self):
        addr = self._do_command()
        val = ~self.mem[addr]
        self.__sub = 1
        self.a += (val + 1)
        self.i += 2

    def jump(self):
        addr = self._do_command()
        self.i = addr - 1

    def jump_if_zero(self):
        addr = self._do_command()
        if self.a == 0:
            self.i = addr - 1
        else:
            self.i += 2

    def jump_if_transfer(self):
        addr = self._do_command()
        if self.p == 1:
            self.i = addr - 1
        else:
            self.i += 2

    def jump_if_not_zero(self):
        addr = self._do_command()
        if self.a != 0:
            self.i = addr - 1
        else:
            self.i += 2

    def jump_if_not_transfer(self):
        addr = self._do_command()
        if self.p == 0:
            self.i = addr - 1
        else:
            self.i += 2

    def left_shift(self):
        addr = self._do_command()
        self.a = self.a << 1
        self.i += 2

    def right_shift(self):
        addr = self._do_command()
        self.a = self.a >> 1
        self.i += 2

    def _sub_with_trasfer(self):
        self.transfer = 1
        self._sub()

    def _not(self):
        addr = self._do_command()
        self.a = ~self.a
        self.i += 2

    def _and(self):
        addr = self._do_command()
        self.a &= self.mem[addr]
        self.i += 2

    def _or(self):
        addr = self._do_command()
        self.a |= self.mem[addr]
        self.i += 2

    def _xor(self):
        addr = self._do_command()
        self.a ^= self.mem[addr]
        self.i += 2

    def _parse_addr(self, val):
        return int(val, 16)

    def _parse_val(self, val):
        return int(val[:-1], 16)

    def load(self, program_name):
        with open(program_name, "r") as f:
            for line in f.readlines():
                if ";" in line:
                    line, comment = line.strip().split(";")
                    comment = comment.strip()
                else:
                    comment = ""
                if len(line.strip()) == 0:
                    continue
                r = line.strip().split()
                if len(r) == 2:
                    addr, data = r
                    bindata = ""
                elif len(r) == 3:
                    addr, data, bindata = r
                addr = self._parse_addr(addr)
                data = self._parse_val(data)
                self.mem[addr] = data
                self.binmem[addr] = bindata
                if comment:
                    self.comment[addr] = comment

    def run(self):
        self.i = 0
        while True:
            if self.mem[self.i] == int("10", 16):
                self._load()
            elif self.mem[self.i] == int("11", 16):
                self._save()
            elif self.mem[self.i] == int("20", 16):
                self._add()
            elif self.mem[self.i] == int("21", 16):
                self._sub()
            elif self.mem[self.i] == int("22", 16):
                self._add_with_transfer()
            elif self.mem[self.i] == int("23", 16):
                self._sub_with_trasfer()
            elif self.mem[self.i] == int("30", 16):
                self.jump()
            elif self.mem[self.i] == int("31", 16):
                self.jump_if_zero()
            elif self.mem[self.i] == int("32", 16):
                self.jump_if_transfer()
            elif self.mem[self.i] == int("33", 16):
                self.jump_if_not_zero()
            elif self.mem[self.i] == int("34", 16):
                self.jump_if_not_transfer()
            elif self.mem[self.i] == int("40", 16):
                self.left_shift()
            elif self.mem[self.i] == int("41", 16):
                self.right_shift()
            elif self.mem[self.i] == int("50", 16):
                self._not()
            elif self.mem[self.i] == int("51", 16):
                self._and()
            elif self.mem[self.i] == int("52", 16):
                self._or()
            elif self.mem[self.i] == int("53", 16):
                self._xor()
            elif self.mem[self.i] == int("FF", 16):
                self._index_use.add(self.i)
                self._index_use.add(self.i+1)
                self._index_use.add(self.i+2)
                break
            else:
                if self.mem[self.i] != 0 or self.i in self._index_use:
                    print(self.mem[self.i])
            self.i += 1
            if self.i >= len(self.mem):
                break

    def _to_hex_addr(self, val):
        return hex(val)[2:].upper()

    def _to_hex_data(self, val):
        return hex(val)[2:].upper()

    def _to_bin_data(self, val):
        return bin(val)[2:]

    def save(self, name_file):
        with open(name_file, "w") as f:
            for i, el in enumerate(self.mem):
                if i in self._index_use:
                    j, el, bel  = self._to_hex_addr(i), self._to_hex_data(el), self._to_bin_data(el)
                    if self.comment[i]:
                        f.write(f"{j:0>4} {el:0>2}h {bel:0>8}  ;{self.comment[i]}\n")
                    else:
                        f.write(f"{j:0>4} {el:0>2}h {bel:0>8}\n")


def main(program_name, file_for_dump_memory):
    c = Computer()
    c.load(program_name)
    c.run()
    c.save(file_for_dump_memory)


if __name__ == '__main__':
    program_name, file_for_dump_memory = sys.argv[1], sys.argv[2]
    main(program_name, file_for_dump_memory)


