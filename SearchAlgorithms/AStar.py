from math import sqrt
from SnakeGame.Movements import Movements


def isGoalState(state: tuple[tuple[int, int], list, Movements], goal: tuple[int, int]) -> bool:
    if state[0] in goal:
        return True
    return False


def getSuccessors(state: tuple[tuple[int, int], list, Movements], table_size: tuple[int, int]):
    successors = []
    pos_head = state[0]
    occupied = state[1][:-1]
    new_state_body = [0] * len(state[1])
    for i in range(len(state[1]) - 1):
        new_state_body[i+1] = state[1][i]
        if i == 0:
            new_state_body[0] = pos_head
    new_state_body = tuple(new_state_body)

    pos_w = (pos_head[0] + 1, pos_head[1])
    if not (pos_w in occupied or pos_w[0] > table_size[0] or state[2] == Movements.EAST):
        successors.append(
            [(pos_w, new_state_body, Movements.WEST), Movements.WEST])

    pos_e = (pos_head[0] - 1, pos_head[1])
    if not (pos_e in occupied or pos_e[0] < 0 or state[2] == Movements.WEST):
        successors.append(
            [(pos_e, new_state_body, Movements.EAST), Movements.EAST])

    pos_n = (pos_head[0], pos_head[1] - 1)
    if not (pos_n in occupied or pos_n[1] < 0 or state[2] == Movements.SOUTH):
        successors.append(
            [(pos_n, new_state_body, Movements.NORTH), Movements.NORTH])

    pos_s = (pos_head[0], pos_head[1] + 1)
    if not (pos_w in occupied or pos_s[1] > table_size[1] or state[2] == Movements.NORTH):
        successors.append(
            [(pos_s, new_state_body, Movements.SOUTH), Movements.SOUTH])
    return successors


def heuristic(state: tuple[tuple[int, int], list, Movements], goal: tuple[int, int]):
    snake_head_x, snake_head_y = state[0]
    fruit_x, fruit_y = goal[0]
    return sqrt((snake_head_x-fruit_x)**2 + (snake_head_y - fruit_y)**2)


def A_star_Search(init_state: tuple[tuple[int, int], tuple, Movements], goal: tuple[int, int], table_size: tuple[int, int]):
    dir = {init_state: [None, 0]}
    queue = PriorityQueue()
    lista = []
    queue.push(tuple(init_state), 0)

    while not queue.isEmpty():
        state = queue.pop()
        if isGoalState(state, goal):
            return list(dir[state][0])
        if state not in lista:
            lista.append(state)
            for s in getSuccessors(state, table_size):
                if dir[state][0] is None:
                    dir[s[0]] = [[s[1]], 1]
                    prio = 1 + heuristic(s[0], goal)
                    queue.push(s[0], prio)
                elif s[0] in dir and dir[s[0]] is not None:
                    if dir[state][1] + 1 < dir[s[0]][1]:
                        n_dic1 = dir[state][0].copy()
                        n_dic2 = dir[state][1]
                        n_dic1.append(s[1])
                        n_dic2 += 1
                        dir[s[0]] = [n_dic1, n_dic2]
                        prio = n_dic2 + heuristic(s[0], goal)
                        queue.update(s[0], prio)
                else:
                    n_dic1 = dir[state][0].copy()
                    n_dic2 = dir[state][1]
                    n_dic1.append(s[1])
                    n_dic2 += 1
                    dir[s[0]] = [n_dic1, n_dic2]
                    prio = n_dic2 + heuristic(s[0], goal)
                    queue.push(s[0], prio)


class PriorityQueue(object):
    def __init__(self):
        self.queue = []

    def __str__(self):
        return ' '.join([str(i) for i in self.queue])

    def isEmpty(self):
        return len(self.queue) == 0

    def push(self, data, prio):
        self.queue.append([data, prio])

    def update(self, data, prio):
        for _, state in enumerate(self.queue):
            if state == data:
                self.queue[_][1] = prio

    def pop(self):
        min_idx = 0
        for i in range(len(self.queue)):
            if self.queue[i][1] < self.queue[min_idx][1]:
                min_idx = i
        item = self.queue[min_idx]
        del self.queue[min_idx]
        return item[0]
