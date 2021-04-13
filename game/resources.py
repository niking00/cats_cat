from collections import deque
from const import OBJECTS, UNITS

class Algorithms:
    def matrix_to_graph(self, matrix):
        graph = {}
        ways = [[0, 1], [0, -1], [1, 0], [-1, 0]]
        for y, i in enumerate(matrix):
            for x, j in enumerate(i):
                if matrix[x][y] not in OBJECTS + [UNITS[0]]:
                    graph[(x, y)] = []
                    for way in ways:
                        if matrix[x + way[0]][y + way[1]] not in OBJECTS + UNITS:
                            graph[(x, y)].append((x + way[0], y + way[1]))
        return graph

    def bfs(self, start, goal, graph):
        queue = deque([start])
        visited = {start: None}

        while queue:
            cur_node = queue.popleft()
            if cur_node == goal:
                break

            next_nodes = graph[cur_node]
            for next_node in next_nodes:
                if next_node not in visited:
                    queue.append(next_node)
                    visited[next_node] = cur_node
        return visited

    def all_way(self, start, goal, visited):
        cur_node = goal
        way = []
        while cur_node != start:
            cur_node = visited[cur_node]
            way.append(cur_node)
        return way
