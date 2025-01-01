#!/usr/bin/env python
import string


class Maze:
    def __init__(self):
        self.tiles = {}
        self.door_keys = {}
        self.doors = {}
        self.nodes = {}
        self.start = None

    @staticmethod
    def from_tiles(tiles):
        maze = Maze()
        maze.tiles = tiles
        for key, value in tiles.items():
            if value in string.ascii_lowercase:
                maze.door_keys[value] = key
            elif value in string.ascii_uppercase:
                maze.doors[value] = key
            elif value == "@":
                maze.start = key
        maze.nodes = {"@": maze.start, **maze.doors, **maze.door_keys}
        return maze

    def print(self):
        max_x = max(x for (x, y) in self.tiles.keys())
        max_y = max(y for (x, y) in self.tiles.keys())
        assert len(self.tiles) == (max_x + 1) * (max_y + 1)
        for y in range(max_y + 1):
            print("".join(self.tiles[(x, y)] for x in range(max_x + 1)))

    def neighbours(self, position):
        x, y = position
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            yield x + dx, y + dy


def parse_input(input_str):
    tiles = {}
    lines = input_str.rstrip().split("\n")
    for y, line in enumerate(lines):
        for x, val in enumerate(line):
            tiles[(x, y)] = val

    return tiles


def read_input(filename):
    with open(filename) as f:
        return f.read()


def distances_from_node(maze, node):
    tile = maze.nodes[node]
    seen = {tile: 0}
    reachable_nodes = {}
    tile_list = [tile]

    while tile_list:
        tile = tile_list.pop(0)
        count = seen[tile]
        for neighbour in maze.neighbours(tile):
            if neighbour in seen:
                continue
            value = maze.tiles[neighbour]
            if value != "#":
                seen[neighbour] = count + 1
                if value in maze.nodes:
                    reachable_nodes[value] = count + 1
                else:
                    tile_list.append(neighbour)

    return reachable_nodes


def main():
    tiles = parse_input(read_input("day18.txt"))
    # tiles = parse_input(testcase_2)
    maze = Maze.from_tiles(tiles)
    maze.print()
    graph = {}
    for node in maze.nodes:
        graph[node] = distances_from_node(maze, node)

    # print_graph(maze, graph)
    print(graph["@"])
    possible = possible_nodes(graph, "@", [])
    print(possible)
    for node in possible:
        print(node, possible_nodes(graph, node, ["@", node]))


def possible_nodes(graph, node, visited):
    return {x: y for x, y in graph[node].items() if x.islower() or x.lower() in visited}


def print_graph(maze, graph):
    for y in maze.nodes:
        l = []
        for x in maze.nodes:
            if x == y:
                val = 0
            else:
                val = graph[x].get(y, 0)
            l.append(val)
        print(",".join(str(x) for x in l))


testcase_1 = """\
#########
#b.A.@.a#
#########
"""

testcase_2 = """\
########################
#f.D.E.e.C.b.A.@.a.B.c.#
######################.#
#d.....................#
########################
"""

testcase_3 = """\
########################
#...............b.C.D.f#
#.######################
#.....@.a.B.c.d.A.e.F.g#
########################
"""

testcase_4 = """\
#################
#i.G..c...e..H.p#
########.########
#j.A..b...f..D.o#
########@########
#k.E..a...g..B.n#
########.########
#l.F..d...h..C.m#
#################
"""

testcase_5 = """\
########################
#@..............ac.GI.b#
###d#e#f################
###A#B#C################
###g#h#i################
########################
"""

if __name__ == "__main__":
    main()
