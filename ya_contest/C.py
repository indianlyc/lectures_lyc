n = int(input())
d_all = {}
d_in = set()
old_time = 1

s = 0

min_name = (0, "ZZZZZZZZZZZ")
a = []

dd = 0

for i in range(n):
    name, time = input().split()
    time = int(time)
    delta_time = time - old_time
    old_time = time
    # for key in d_in:
    #     d_all[key] += delta_time
    s += len(d_in) * delta_time
    min_name = (min_name[0] - delta_time, min_name[1])
    if name not in d_all and name not in d_in:
        d_all[name] = (0, time)
        d_in.add(name)
        min_name = min((0, name), min_name)
    elif name not in d_in:
        d_in.add(name)
        d_all[name] = (d_all[name][0], time)
        s += d_all[name][0]
        min_name = min((-d_all[name][0], name), min_name)
    else:
        d_in.remove(name)
        d_all[name] = (time - d_all[name][1] + d_all[name][0], time)
        s -= d_all[name][0]
        if name == min_name[1]:
            min_name = min([(-(time - d_all[key][1] + d_all[key][0]), key) for key in d_in])
    a.append(f"{min_name[1]} {s + 2 * min_name[0]}")
print("\n".join(a))