import random


def get_max(l: list[int]) -> int:
    if len(l):
        m = l[0]
        for k in l[1:]:
            if k > m:
                m = k
        return m
    else:
        return None
    
    
if __name__ == "__main__":
    a = [random.randint(-100, 100) for i in range(10)]
    print(a)
    print(get_max(a))