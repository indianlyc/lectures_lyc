import collections


class City:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self, city):
        return abs(self.x - city.x) + abs(self.y - city.y)


def bfs(graph, root):
    visited, queue = set(), collections.deque([root])
    visited.add(root)
    parents = {}

    while queue:
        vertex = queue.popleft()
        for neighbour in graph[vertex]:
            if neighbour not in visited:
                visited.add(neighbour)
                queue.append(neighbour)
                parents[neighbour] = vertex
    return parents


class Graph:
    def __init__(self, cities, k):
        self.cities = cities
        self.k = k

    def __getitem__(self, arg):
        for i_city in cities:
            if i_city != arg:
                if cities[arg].distance(cities[i_city]) <= k:
                    yield i_city


if __name__ == "__main__":
    n = int(input())
    cities = {}
    for i in range(n):
        x, y = map(int, input().split())
        cities[i+1] = City(x, y)
    k = int(input())
    from_city, to_city = map(int, input().split())
    if from_city == to_city:
        print(0)
    else:
        graph = Graph(cities, k)
        parents = bfs(graph, from_city)
        if to_city not in parents:
            print(-1)
        else:
            l = 0
            p = to_city
            while p in parents:
                p = parents[p]
                l += 1
            print(l)