from .BaseAgent import BaseAgent

Tv = super
Tu = int
TW = None
Tb = enumerate
TX = abs
Tx = range
To = len
TB = False
Ts = True
TR = print
Ti = set
from environment.game import Game
from environment.models.constants import Direction

Tk = Direction.RIGHT
TH = Direction.DOWN
Ta = Direction.LEFT
TC = Direction.UP
import numpy

Tw = numpy.zeros
from heapq import heappop, heappush


class TL(BaseAgent):
    def __init__(T):
        Tv().__init__()
        T.goal_x = 0
        T.goal_y = 0
        T.last_enemy_head_coord_x = 0
        T.last_enemy_head_coord_y = 0

    def Te(T, game: Game, snake_idx: Tu):
        G = []
        I = TW
        for Y, snake in Tb(game.snakes):
            if not snake.body:
                continue
            if Y == snake_idx:
                e = snake
            else:
                f = snake
                G = f.body
                S = G[0].x
                J = G[0].y
        P = e.body
        N = P[0].x
        L = P[0].y
        C = P[-1].x
        a = P[-1].x
        H = game.width
        k = game.height
        w = game.get_fruits()
        v = H * 2 + k * 2
        for f in w:
            u = f.x
            W = f.y
            b = TX(L - W) + TX(N - u)
            if b < v:
                v = b
                X = f.x
                x = f.y
        o = 0
        for f in w:
            u = f.x
            W = f.y
            b = TX(L - W) + TX(N - u)
            for Y, snake in Tb(game.snakes):
                if not snake.body:
                    continue
                if Y == snake_idx:
                    continue
                else:
                    f = snake
                    G = f.body
                    S = G[0].x
                    J = G[0].y
                    B = TX(J - x) + TX(S - X)
                    if B <= b:
                        o += 0
                        continue
                    else:
                        b = TX(L - W) + TX(N - u)
                        o += 1
                        if b < v:
                            v = b
                            X = f.x
                            x = f.y
        if o == 0:
            for f in w:
                u = f.x
                W = f.y
                b = TX(L - W) + TX(N - u)
                if b < v:
                    v = b
                    X = f.x
                    x = f.y
        s = Tw((H, k))
        R = [n for n in Tx(100)]
        for s in P:
            s[s.x, s.y] = 1
        if To(game.snakes) > 1:
            for e in G:
                s[e.x, e.y] = 1
        for Y, snake in Tb(game.snakes):
            if not snake.body:
                continue
            if Y == snake_idx:
                continue
            else:
                f = snake
                G = f.body
                S = G[0].x
                J = G[0].y
                for e in G:
                    s[e.x, e.y] = 1
                if To(G) >= To(P):
                    for f in w:
                        if T.TJ(s, (S, J), (f.x, f.y)) == TB:
                            continue
                        else:
                            i = T.TJ(s, (S, J), (f.x, f.y))
                            if To(i) <= 3:
                                if To(i) < To(R):
                                    R = i
                                    z = R[-1]
                                    V = z[0]
                                    E = z[1]
                                    s[V, E] = 1
        M = [n for n in Tx(100)]
        y = [width for width in Tx(H)]
        p = [height for height in Tx(k)]
        for w in y:
            s[w, 0] = 1
            s[w, k - 1] = 1
        for h in p:
            s[0, h] = 1
            s[H - 1, h] = 1
        for f in w:
            if T.TJ(s, (N, L), (f.x, f.y)) == TB:
                continue
            else:
                n = T.TJ(s, (N, L), (f.x, f.y))
                m = Ts
                if To(n) < To(M):
                    M = n
                    T.goal_x = f.x
                    T.goal_y = f.y
        for Y, snake in Tb(game.snakes):
            if not snake.body:
                continue
            if Y == snake_idx:
                continue
            else:
                f = snake
                G = f.body
                S = G[0].x
                J = G[0].y
                if T.TJ(s, (N, L), (T.TN(S, J, T.last_enemy_head_coord_x, T.last_enemy_head_coord_y))) == TB:
                    continue
                else:
                    if T.TJ(s, (N, L), (T.TN(S, J, T.last_enemy_head_coord_x, T.last_enemy_head_coord_y))) == []:
                        continue
                    else:
                        if To(P) > To(G) + 1:
                            n = T.TJ(s, (N, L), (T.TN(S, J, T.last_enemy_head_coord_x, T.last_enemy_head_coord_y)))
                            if To(n) < To(M):
                                TR('ATTACKING!')
                                M = n
                                T.goal_x = S
                                T.goal_y = J
        r = [n for n in Tx(100)]
        s[T.goal_x, T.goal_y] = 9
        U = 0
        if M != [n for n in Tx(100)]:
            for f in w:
                for p in M:
                    s[p[0], p[1]] = 1
                if f.x == T.goal_x and f.y == T.goal_y:
                    U += 0
                else:
                    if T.TJ(s, (T.goal_x, T.goal_y), (f.x, f.y)) == []:
                        U += 0
                    else:
                        if T.TJ(s, (T.goal_x, T.goal_y), (f.x, f.y)) == TB:
                            U += 0
                            if T.TJ(s, (N, L), (f.x, f.y)) != TB:
                                n = T.TJ(s, (N, L), (f.x, f.y))
                                if To(n) < To(r):
                                    r = n
                            else:
                                continue
                        else:
                            U += 1
            for p in M:
                s[p[0], p[1]] = 2
            s[T.goal_x, T.goal_y] = 9
            if U == 0:
                if r != [n for n in Tx(100)]:
                    M = r
                    U += 1
        if U == 0:
            for w in y:
                s[w, 0] = 0
                s[w, k - 1] = 0
            for h in p:
                s[0, h] = 0
                s[H - 1, h] = 0
            for s in P:
                s[s.x, s.y] = 1
            if To(game.snakes) > 1:
                for e in G:
                    s[e.x, e.y] = 1
            for f in w:
                if T.TJ(s, (N, L), (f.x, f.y)) == TB:
                    continue
                else:
                    n = T.TJ(s, (N, L), (f.x, f.y))
                    m = Ts
                    if To(n) < To(M):
                        M = n
                        T.goal_x = f.x
                        T.goal_y = f.y
        if M == [n for n in Tx(100)]:
            s[C, a] = 0
            if T.TJ(s, (N, L), (C, a)) == TB:
                TR('Cant find tail!')
            else:
                n = T.TJ(s, (N, L), (C, a))
                if To(n) > 1:
                    M = n
                    TR('Chasing tail!')
        s[C, a] = 1
        if M == [n for n in Tx(100)]:
            M = []
        if M == []:
            for h in p:
                for w in y:
                    c = T.TJ(s, (N, L), (w, h))
                    if c != TB and c != []:
                        TR('found')
                        if To(c) > To(M):
                            M = c
                            TR('PATH:', M)
        for Y, snake in Tb(game.snakes):
            if not snake.body:
                continue
            if Y == snake_idx:
                continue
            else:
                T.last_enemy_head_coord_x = S
                T.last_enemy_head_coord_y = J
        if M != []:
            j = M[-1]
            d = j[0]
            A = j[1]
            I = T.TP(d, A, N, L)
        else:
            TR()
            TR('DEAD!')
            TR()
        return I

    def Tf(T, snake_idx: Tu):
        return 'Finn Agent'

    def TS(T, a, b):
        return TX(b[0] - a[0]) + TX(b[1] - a[1])

    def TJ(T, array, start, goal):
        q = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        g = Ti()
        t = {}
        Q = {start: 0}
        K = {start: T.TS(start, goal)}
        h = []
        heappush(h, (K[start], start))
        while h:
            l = heappop(h)[1]
            if l == goal:
                F = []
                while l in t:
                    F.append(l)
                    l = t[l]
                return F
            g.add(l)
            for i, j in q:
                D = l[0] + i, l[1] + j
                O = Q[l] + T.TS(l, D)
                if 0 <= D[0] < array.shape[0]:
                    if 0 <= D[1] < array.shape[1]:
                        if array[D[0]][D[1]] == 1:
                            continue
                    else:
                        continue
                else:
                    continue
                if D in g and O >= Q.get(D, 0):
                    continue
                if O < Q.get(D, 0) or D not in [i[1] for i in h]:
                    t[D] = l
                    Q[D] = O
                    K[D] = O + T.TS(D, goal)
                    heappush(h, (K[D], D))
        return TB

    def TP(T, move_x, move_y, current_x, current_y):
        if move_y < current_y:
            TG = TC
            return TG
        else:
            if move_x < current_x:
                TG = Ta
                return TG
            else:
                if move_y > current_y:
                    TG = TH
                    return TG
                else:
                    if move_x > current_x:
                        TG = Tk
                        return TG

    def TN(T, move_x, move_y, current_x, current_y):
        if move_y < current_y:
            TI = move_y - 1
            return TI, move_x
        else:
            if move_x < current_x:
                TY = move_x - 1
                return TY, move_y
            else:
                if move_y > current_y:
                    TI = move_y + 1
                    return TI, move_x
                else:
                    if move_x > current_x:
                        TY = move_x + 1
                        return TY, move_y
# Created by pyminifier (https://github.com/liftoff/pyminifier)
