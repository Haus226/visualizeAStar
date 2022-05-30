from random import shuffle, randrange

def inMap(map_, node):
    if 1 <= node[0] < len(map_)  and 1 <= node[1] < len(map_[0]):
        return True
    return False

def isWall(map_, node):
    if map_[node[0]][node[1]]:
        return False
    return True

def Children(map_, node):
    children = []
    actions = {"up": (node[0] - 2, node[1]),
               "down": (node[0] + 2, node[1]),
               "right": (node[0], node[1] + 2),
               "left": (node[0], node[1] - 2)}

    for action in actions:
        if inMap(map_, actions[action]) and isWall(map_, actions[action]):
            children.append(actions[action])
    return children

def BackTracking(map_):
    cur = (
            randrange(1, len(map_) - 1, 2),
            randrange(1, len(map_[0]) - 1, 2)
                )
    if not (len(map_) & 1) and not (len(map_[0]) & 1):
        print("Hi")
        cur = (randrange(1, len(map_) - 1, 2), randrange(1, len(map_[0]) - 1, 2))


    track = [cur]
    print(cur)
    path = [cur]
    map_[cur[0]][cur[1]] = 1
    while track:
        cur = track[-1]
        children = Children(map_, cur)
        shuffle(children)
        if not len(children):
            track = track[:-1]
        else:
            child = children[0]
            map_[child[0]][child[1]] = 1
            map_[(cur[0] + child[0]) // 2][(cur[1] + child[1]) // 2] = 1
            track += [child]
            path.append(((cur[0] + child[0]) // 2, (cur[1] + child[1]) // 2))
            path.append(child)
    return path