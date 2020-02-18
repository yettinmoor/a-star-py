import heapq


class Node:

    openedNodes = []
    closedNodes = []
    target = None
    grid = {}

    def __init__(self, x, y, state):
        self.x = x
        self.y = y
        self.walkable = state != 'obstacle'
        self.gcost = float('inf')
        self.parent = None

        Node.grid[(x, y)] = self

        if (state == 'target'):
            Node.target = self
        elif (state == 'start'):
            heapq.heappush(Node.openedNodes, self)
            self.gcost = 0


    @staticmethod
    def generate_grid(filename):
        states = { 'X': 'obstacle', '@': 'target', 'O': 'start' }
        with open(filename) as f:
            Node.ascii_grid = [r.strip() for r in f.readlines()]
            for y, row in enumerate(Node.ascii_grid):
                for x, node in enumerate(row):
                    Node(x, y, states.get(node, None))

    @property
    def cost(self):
        return self.gcost + self.hcost

    @property
    def hcost(self):
        return self.distance(Node.target)

    def __lt__(self, other):
        return self.cost < other.cost or self.cost == other.cost and self.hcost < other.hcost

    def distance(self, node):
        dx, dy = abs(self.x - node.x), abs(self.y - node.y)
        return 14 * min(dx, dy) + 10 * abs(dx - dy)

    def update_neighbors(self):

        neighbors = []
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                neighbors.append(Node.grid.get((self.x + dx, self.y + dy), None))

        for neighbor in [n for n in neighbors if n and n.walkable and n not in Node.closedNodes]:

            if (gcost := self.gcost + self.distance(neighbor)) < neighbor.gcost:
                neighbor.parent = self
                neighbor.gcost = gcost
                if neighbor not in Node.openedNodes:
                    heapq.heappush(Node.openedNodes, neighbor)

    @staticmethod
    def get_next():
        n = heapq.heappop(Node.openedNodes)
        Node.closedNodes.append(n)
        return n

    @staticmethod
    def find_path():
        while Node.openedNodes and (current := Node.get_next()) is not Node.target:
            current.update_neighbors()

    @staticmethod
    def print_path():

        current = Node.target
        path = []

        while (current := current.parent) and current.parent:
            path.append((current.x, current.y))

        for row in [['!' if (x, y) in path else n for x, n in enumerate(row)] for y, row in enumerate(Node.ascii_grid)]:
            print(''.join(row))


Node.generate_grid('astar.txt')
Node.find_path()
Node.print_path()
