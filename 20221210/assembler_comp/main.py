import sys

d = {
    "10": "Загрузить",
    "11": "Сохранить",
    "20": "Сложить",
    "21": "Вычесть",
    "-1": "Остановить",
}
class Computer:
    def __init__(self, memory_size=65536):
        self._index_use = set()
        self.mem = [0] * memory_size
        self.a = 0  # аккумулятор (защелка)

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
        addr = self._do_command()
        self.a += self.mem[addr]
        self.i += 2

    def _sub(self):
        addr = self._do_command()
        self.a -= self.mem[addr]
        self.i += 2

    def _parse_addr(self, val):
        return int(val, 16)

    def _parse_val(self, val):
        return int(val[:-1], 16)

    def load(self, program_name):
        with open(program_name, "r") as f:
            for line in f.readlines():
                addr, data = line.strip().split()
                addr = self._parse_addr(addr)
                data = self._parse_val(data)
                self.mem[addr] = data

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
            elif self.mem[self.i] == int("FF", 16):
                break
            else:
                if self.mem[self.i] !=0 or self.i in self._index_use:
                    print(self.mem[self.i])
            self.i += 1
            if self.i >= len(self.mem):
                break

    def _to_hex_addr(self, val):
        return hex(val)[2:]

    def _to_hex_data(self, val):
        return hex(val)[2:]

    def save(self, name_file):
        with open(name_file, "w") as f:
            for i, el in enumerate(self.mem):
                if i in self._index_use:
                    i, el  = self._to_hex_addr(i), self._to_hex_data(el)
                    f.write(f"{i:0>4} {el:0>2}h\n")


def main(program_name, file_for_dump_memory):
    c = Computer()
    c.load(program_name)
    c.run()
    c.save(file_for_dump_memory)


if __name__ == '__main__':
    program_name, file_for_dump_memory = sys.argv[1], sys.argv[2]
    main(program_name, file_for_dump_memory)


