import heapq

GridLocation = (int, int)

class SquareGrid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.walls = []

    def in_bounds(self, id):
        (x, y) = id
        return 0 <= x < self.width and 0 <= y < self.height

    def passable(self, id):
        return id not in self.walls

    def neighbors(self, id):
        (x, y) = id
        results = [(x+1, y), (x, y-1), (x-1, y), (x, y+1)]
        if (x + y) % 2 == 0: results.reverse()
        results = filter(self.in_bounds, results)
        results = filter(self.passable, results)
        return results
def from_id_width(id, width):
    return (id % width, id // width)

class GridWithWeights(SquareGrid):
    def __init__(self, width: int, height: int):
        super().__init__(width, height)
        self.weights = dict()

    def cost(self, from_node: GridLocation, to_node: GridLocation) -> float:
        return self.weights.get(to_node, 1)

def draw_tile(graph, id, style):
    r = "_傘_"
    if 'number' in style and id in style['number']: r = " %-2d" % style['number'][id]
    if 'point_to' in style and style['point_to'].get(id, None) is not None:
        (x1, y1) = id
        (x2, y2) = style['point_to'][id]
        if x2 == x1 + 1: r = " > "
        if x2 == x1 - 1: r = " < "
        if y2 == y1 + 1: r = " v "
        if y2 == y1 - 1: r = " ^ "
    if 'path' in style and id in style['path']:   r = "_火_"
    if 'start' in style and id == style['start']: r = "_人_"
    if 'goal' in style and id == style['goal']:   r = "_人_"
    if id in graph.walls: r = "_田_"
    return r

def draw_grid(graph, **style):
    thegrid = "_"
    for i in range(graph.width):
        if i < 10:
            thegrid += ("_{}__".format(i))
        if (9<i<100):
            thegrid += ("{}__".format(i))
        if i > 99:
            thegrid += ("{}_".format(i))
    thegrid += "___\n"
    for y in range(graph.height):
        thegrid += "|"
        for x in range(graph.width):
            thegrid += ("%s" % draw_tile(graph, (x, y), style))
        if y < 10:
            thegrid += ("|_{}_|".format(y))
        if (9<y<100):
            thegrid += ("|_{}|".format(y))
        if y > 99:
            thegrid += ("|{}|".format(y))
        thegrid += "\n"
    #thegrid += ("~~~" * graph.width+2)
    return thegrid

class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]

def heuristic(a, b):
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)

def a_star_search(graph, start, goal):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        current = frontier.get()

        if current == goal:
            break

        for next in graph.neighbors(current):
            new_cost = cost_so_far[current] + graph.cost(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(goal, next)
                frontier.put(next, priority)
                came_from[next] = current

    return came_from, cost_so_far

def reconstruct_path(came_from, start, goal):
    current = goal
    path = [current]
    while current != start:
        current = came_from[current]
        path.append(current)
    path.append(start)
    path.reverse()
    return path