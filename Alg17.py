import random as r
import Asta
def rookmechanics(width, length):
    n = width
    m = length
    plane = Asta.GridWithWeights(n, m)
    walls = []
    #[[0] * n for i in range(m)]
    for i in range(m):
        for j in range(n):
            if r.random() < 0.2:
                walls.append((i, j))
    plane.walls = walls
    return plane


def straightener(path):
    straightpath = path
    excess = []
    for i in range(1, len(straightpath)-1):
        if (straightpath[i-1][0] < straightpath[i][0] < straightpath[i+1][0]) or (straightpath[i-1][0] > straightpath[i][0] > straightpath[i+1][0]) or (straightpath[i-1][1] < straightpath[i][1] < straightpath[i+1][1]) or (straightpath[i-1][1] > straightpath[i][1] > straightpath[i+1][1]):
            excess.append(i)
    excess.reverse()
    for item in excess:
        straightpath.pop(item)
    return straightpath


def pathteller(path):
    thepathis = ""
    for i in range(1, len(path)//2):
        thepathis += ("{}".format(i))
        thepathis += ("Move for the 1st rook: {}\n".format(path[i]))
        thepathis += ("{}".format(i))
        thepathis += ("Move for the 2nd rook: {}\n".format(path[len(path)-i]))
    if len(path)%2 == 1:
        thepathis += ("{}".format((len(path)//2)+1))
        thepathis += ("Move for the 1st rook: {}\n".format(path[(len(path)//2)+1]))
    return thepathis
