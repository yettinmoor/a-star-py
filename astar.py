class Node:

    target = None
    field = {}

    def __init__(self, x, y, type_):
        self.x = x
        self.y = y
        Node.field[(x, y)] = self

        if (type_ == 'target'):
            self.type = 'unseen'
            Node.target = self
        else:
            self.type = type_

        self.gcost = self.hcost = 0
        self.parent = None

    @property
    def cost(self):
        return self.gcost + self.hcost

    def cost_to_node(self, node):
        dx, dy = abs(self.x - node.x), abs(self.y - node.y)
        return 14 * min(dx, dy) + 10 * abs(dx - dy)

    def get_neighbors(self):
        neighbors = []
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                neighbors.append(Node.field.get((self.x + dx, self.y + dy), None))
        return [n for n in neighbors if n]

    def get_path(self):
        node = self
        path = []
        while (node := node.parent):
            path.append(node)
        return path

    @staticmethod
    def filter_types(type_):
        return [n for n in Node.field.values() if n.type == type_]


def generate_field(filename):

    types = { 'X': 'obstacle', '@': 'target', 'O': 'open', '.': 'unseen', '!': 'closed' }

    with open(filename) as f:
        ascii_field = [r.strip() for r in f.readlines()]
        for y, row in enumerate(ascii_field):
            for x, node in enumerate(row):
                Node(x, y, types[node])

        return ascii_field


def find_path():

    while True:

        current = None
        for n in [n for n in Node.field.values() if n.type == 'open']:
            if not current or n.cost < current.cost:
                current = n

        if current is Node.target:
            break

        current.type = 'closed'

        for n in current.get_neighbors():

            if n and n.type in ['open', 'unseen']:

                new_gcost = current.gcost + current.cost_to_node(n)
                new_hcost = n.cost_to_node(Node.target)

                if n.type == 'unseen' or new_gcost + new_hcost < n.cost:
                    n.type = 'open'
                    n.gcost = new_gcost
                    n.hcost = new_hcost
                    n.parent = current


def print_completed_path(ascii_field):

    pathed_field = [[c for c in row] for row in ascii_field]

    for node in Node.target.get_path():
        pathed_field[node.y][node.x] = '!'

    for row in pathed_field:
        print(''.join(row))


ascii_field = generate_field('astar.txt')
find_path()
print_completed_path(ascii_field)
