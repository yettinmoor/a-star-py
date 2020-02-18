class Node:

    def __init__(self, x, y, type_):
        self.x = x
        self.y = y
        self.type = type_
        self.fcost = self.hcost = 0
        self.parent = None

    @property
    def cost(self):
        return self.fcost + self.hcost

    def __equals__(self, o):
        return self.x == o.x and self.y == o.y


class Field:

    def __init__(self, filename):

        types = { 'X': 'obstacle', '@': 'target', 'O': 'open', '.': 'unseen', '!': 'closed' }
        with open(filename) as f:
            self.ascii_field = [r.strip() for r in f.readlines()]

        self.nodes = [[Node(x, y, types[node]) for x, node in enumerate(row)] for y, row in enumerate(self.ascii_field)]

        # Remember target position, set it to unseen
        for n in sum(self.nodes, []):
            if n.type == 'target':
                self.target = n
                n.type = 'unseen'

    def filter_types(self, type_):
        return [n for row in self.nodes for n in row if n.type == type_]

    def get_neighbors(self, node):
        neighbors = []
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                try:
                    neighbors.append(self.nodes[node.y + dy][node.x + dx])
                except IndexError:
                    continue
        return neighbors

    def cost_to_target(self, node):
        dx, dy = abs(node.x - self.target.x), abs(node.y - self.target.y)
        return 14 * min(dx, dy) + 10 * abs(dx - dy)

    def get_path(self):
        node = field.target
        path = []
        while (node := node.parent):
            path.append(node)
        return path

    def print(self):
        pathed_field = [[c for c in row] for row in self.ascii_field]
        for node in self.get_path():
            pathed_field[node.y][node.x] = '!'
        for row in pathed_field:
            print(''.join(row))


field = Field('astar.txt')

while True:

    current = None
    for n in field.filter_types('open'):
        if not current or n.cost < current.cost:
            current = n

    if current == field.target:
        break;

    current.type = 'closed'

    # Loop through neighbors
    for n in field.get_neighbors(current):

        if n.type in ['open', 'unseen']:

            # G cost
            new_fcost = current.fcost + (10 if (current.x - n.x) * (current.y - n.y) == 0 else 14)
            new_hcost = field.cost_to_target(n)

            if n.type == 'unseen' or new_fcost + new_hcost < n.cost:
                n.type = 'open'
                n.fcost = new_fcost
                n.hcost = new_hcost
                n.parent = current

field.print()
