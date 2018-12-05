from .BaseAgent import BaseAgent
from environment.game import Game
from environment.models.constants import Direction
import numpy
from heapq import heappop, heappush


class FinnAgent(BaseAgent):
    def __init__(QDKrSREt):
        super().__init__()
        QDKrSREt.goal_x = 0
        QDKrSREt.goal_y = 0
        QDKrSREt.last_enemy_head_coord_x = 0
        QDKrSREt.last_enemy_head_coord_y = 0

    def act(QDKrSREt, game: Game, snake_idx: int):
        QDKrSREC = []
        QDKrSREe = None
        for QDKrSREf, snake in enumerate(game.snakes):
            if not snake.body:
                continue
            if QDKrSREf == snake_idx:
                QDKrSREM = snake
            else:
                QDKrSREn = snake
                QDKrSREC = QDKrSREn.body
                QDKrSREF = QDKrSREC[0].x
                QDKrSREL = QDKrSREC[0].y
        QDKrSREm = QDKrSREM.body
        QDKrSREz = QDKrSREm[0].x
        QDKrSREG = QDKrSREm[0].y
        QDKrSREo = QDKrSREm[-1].x
        QDKrSREW = QDKrSREm[-1].x
        QDKrSREg = game.width
        QDKrSREU = game.height
        QDKrSREs = game.get_fruits()
        QDKrSREJ = QDKrSREg * 2 + QDKrSREU * 2
        for QDKrSREV in QDKrSREs:
            QDKrSREx = QDKrSREV.x
            QDKrSREd = QDKrSREV.y
            QDKrSREN = abs(QDKrSREG - QDKrSREd) + abs(QDKrSREz - QDKrSREx)
            if QDKrSREN < QDKrSREJ:
                QDKrSREJ = QDKrSREN
                QDKrSREv = QDKrSREV.x
                QDKrSREX = QDKrSREV.y
        QDKrSREj = 0
        for QDKrSREV in QDKrSREs:
            QDKrSREx = QDKrSREV.x
            QDKrSREd = QDKrSREV.y
            QDKrSREN = abs(QDKrSREG - QDKrSREd) + abs(QDKrSREz - QDKrSREx)
            for QDKrSREf, snake in enumerate(game.snakes):
                if not snake.body:
                    continue
                if QDKrSREf == snake_idx:
                    continue
                else:
                    QDKrSREn = snake
                    QDKrSREC = QDKrSREn.body
                    QDKrSREF = QDKrSREC[0].x
                    QDKrSREL = QDKrSREC[0].y
                    QDKrSREy = abs(QDKrSREL - QDKrSREX) + abs(QDKrSREF - QDKrSREv)
                    if QDKrSREy <= QDKrSREN:
                        QDKrSREj += 0
                        continue
                    else:
                        QDKrSREN = abs(QDKrSREG - QDKrSREd) + abs(QDKrSREz - QDKrSREx)
                        QDKrSREj += 1
                        if QDKrSREN < QDKrSREJ:
                            QDKrSREJ = QDKrSREN
                            QDKrSREv = QDKrSREV.x
                            QDKrSREX = QDKrSREV.y
        if QDKrSREj == 0:
            for QDKrSREV in QDKrSREs:
                QDKrSREx = QDKrSREV.x
                QDKrSREd = QDKrSREV.y
                QDKrSREN = abs(QDKrSREG - QDKrSREd) + abs(QDKrSREz - QDKrSREx)
                if QDKrSREN < QDKrSREJ:
                    QDKrSREJ = QDKrSREN
                    QDKrSREv = QDKrSREV.x
                    QDKrSREX = QDKrSREV.y
        QDKrSREP = numpy.zeros((QDKrSREg, QDKrSREU))
        QDKrSREY = [n for n in range(100)]
        for QDKrSREA in QDKrSREm:
            QDKrSREP[QDKrSREA.x, QDKrSREA.y] = 1
        if len(game.snakes) > 1:
            for QDKrSREH in QDKrSREC:
                QDKrSREP[QDKrSREH.x, QDKrSREH.y] = 1
        for QDKrSREf, snake in enumerate(game.snakes):
            if not snake.body:
                continue
            if QDKrSREf == snake_idx:
                continue
            else:
                QDKrSREn = snake
                QDKrSREC = QDKrSREn.body
                QDKrSREF = QDKrSREC[0].x
                QDKrSREL = QDKrSREC[0].y
                for QDKrSREH in QDKrSREC:
                    QDKrSREP[QDKrSREH.x, QDKrSREH.y] = 1
                if len(QDKrSREC) >= len(QDKrSREm):
                    for QDKrSREV in QDKrSREs:
                        if not QDKrSREt.astar(QDKrSREP, (QDKrSREF, QDKrSREL), (QDKrSREV.x, QDKrSREV.y)):
                            continue
                        else:
                            QDKrSREp = QDKrSREt.astar(QDKrSREP, (QDKrSREF, QDKrSREL), (QDKrSREV.x, QDKrSREV.y))
                            if len(QDKrSREp) <= 3:
                                if len(QDKrSREp) < len(QDKrSREY):
                                    QDKrSREY = QDKrSREp
                                    QDKrSRET = QDKrSREY[-1]
                                    QDKrSREi = QDKrSRET[0]
                                    QDKrSREc = QDKrSRET[1]
                                    QDKrSREP[QDKrSREi, QDKrSREc] = 1
        QDKrSREa = [n for n in range(100)]
        QDKrSREw = [QDKrSREu for QDKrSREu in range(QDKrSREg)]
        QDKrSREl = [QDKrSREI for QDKrSREI in range(QDKrSREU)]
        for QDKrSREu in QDKrSREw:
            QDKrSREP[QDKrSREu, 0] = 1
            QDKrSREP[QDKrSREu, QDKrSREU - 1] = 1
        for QDKrSREI in QDKrSREl:
            QDKrSREP[0, QDKrSREI] = 1
            QDKrSREP[QDKrSREg - 1, QDKrSREI] = 1
        for QDKrSREV in QDKrSREs:
            if not QDKrSREt.astar(QDKrSREP, (QDKrSREz, QDKrSREG), (QDKrSREV.x, QDKrSREV.y)):
                continue
            else:
                QDKrSREh = QDKrSREt.astar(QDKrSREP, (QDKrSREz, QDKrSREG), (QDKrSREV.x, QDKrSREV.y))
                QDKrSREb = True
                if len(QDKrSREh) < len(QDKrSREa):
                    QDKrSREa = QDKrSREh
                    QDKrSREt.goal_x = QDKrSREV.x
                    QDKrSREt.goal_y = QDKrSREV.y
        for QDKrSREf, snake in enumerate(game.snakes):
            if not snake.body:
                continue
            if QDKrSREf == snake_idx:
                continue
            else:
                QDKrSREn = snake
                QDKrSREC = QDKrSREn.body
                QDKrSREF = QDKrSREC[0].x
                QDKrSREL = QDKrSREC[0].y
                if not QDKrSREt.astar(QDKrSREP, (QDKrSREz, QDKrSREG), (
                QDKrSREt.calculate_next_move(QDKrSREF, QDKrSREL, QDKrSREt.last_enemy_head_coord_x,
                                             QDKrSREt.last_enemy_head_coord_y))):
                    continue
                else:
                    if not QDKrSREt.astar(QDKrSREP, (QDKrSREz, QDKrSREG), (
                    QDKrSREt.calculate_next_move(QDKrSREF, QDKrSREL, QDKrSREt.last_enemy_head_coord_x,
                                                 QDKrSREt.last_enemy_head_coord_y))):
                        continue
                    else:
                        if len(QDKrSREm) > len(QDKrSREC) + 1:
                            QDKrSREh = QDKrSREt.astar(QDKrSREP, (QDKrSREz, QDKrSREG), (
                                QDKrSREt.calculate_next_move(QDKrSREF, QDKrSREL, QDKrSREt.last_enemy_head_coord_x,
                                                             QDKrSREt.last_enemy_head_coord_y)))
                            if len(QDKrSREh) < len(QDKrSREa):
                                print('ATTACKING!')
                                QDKrSREa = QDKrSREh
                                QDKrSREt.goal_x = QDKrSREF
                                QDKrSREt.goal_y = QDKrSREL
        QDKrSREk = [n for n in range(100)]
        QDKrSREP[QDKrSREt.goal_x, QDKrSREt.goal_y] = 9
        QDKrSREB = 0
        if QDKrSREa != [n for n in range(100)]:
            for QDKrSREV in QDKrSREs:
                for QDKrSREO in QDKrSREa:
                    QDKrSREP[QDKrSREO[0], QDKrSREO[1]] = 1
                if QDKrSREV.x == QDKrSREt.goal_x and QDKrSREV.y == QDKrSREt.goal_y:
                    QDKrSREB += 0
                else:
                    if QDKrSREt.astar(QDKrSREP, (QDKrSREt.goal_x, QDKrSREt.goal_y), (QDKrSREV.x, QDKrSREV.y)) == []:
                        QDKrSREB += 0
                    else:
                        if QDKrSREt.astar(QDKrSREP, (QDKrSREt.goal_x, QDKrSREt.goal_y),
                                          (QDKrSREV.x, QDKrSREV.y)) == False:
                            QDKrSREB += 0
                            if QDKrSREt.astar(QDKrSREP, (QDKrSREz, QDKrSREG), (QDKrSREV.x, QDKrSREV.y)) != False:
                                QDKrSREh = QDKrSREt.astar(QDKrSREP, (QDKrSREz, QDKrSREG), (QDKrSREV.x, QDKrSREV.y))
                                if len(QDKrSREh) < len(QDKrSREk):
                                    QDKrSREk = QDKrSREh
                            else:
                                continue
                        else:
                            QDKrSREB += 1
            for QDKrSREO in QDKrSREa:
                QDKrSREP[QDKrSREO[0], QDKrSREO[1]] = 2
            QDKrSREP[QDKrSREt.goal_x, QDKrSREt.goal_y] = 9
            if QDKrSREB == 0:
                if QDKrSREk != [n for n in range(100)]:
                    QDKrSREa = QDKrSREk
                    QDKrSREB += 1
        if QDKrSREB == 0:
            for QDKrSREu in QDKrSREw:
                QDKrSREP[QDKrSREu, 0] = 0
                QDKrSREP[QDKrSREu, QDKrSREU - 1] = 0
            for QDKrSREI in QDKrSREl:
                QDKrSREP[0, QDKrSREI] = 0
                QDKrSREP[QDKrSREg - 1, QDKrSREI] = 0
            for QDKrSREA in QDKrSREm:
                QDKrSREP[QDKrSREA.x, QDKrSREA.y] = 1
            if len(game.snakes) > 1:
                for QDKrSREH in QDKrSREC:
                    QDKrSREP[QDKrSREH.x, QDKrSREH.y] = 1
            for QDKrSREV in QDKrSREs:
                if QDKrSREt.astar(QDKrSREP, (QDKrSREz, QDKrSREG), (QDKrSREV.x, QDKrSREV.y)) == False:
                    continue
                else:
                    QDKrSREh = QDKrSREt.astar(QDKrSREP, (QDKrSREz, QDKrSREG), (QDKrSREV.x, QDKrSREV.y))
                    QDKrSREb = True
                    if len(QDKrSREh) < len(QDKrSREa):
                        QDKrSREa = QDKrSREh
                        QDKrSREt.goal_x = QDKrSREV.x
                        QDKrSREt.goal_y = QDKrSREV.y
        if QDKrSREa == [n for n in range(100)]:
            QDKrSREP[QDKrSREo, QDKrSREW] = 0
            if QDKrSREt.astar(QDKrSREP, (QDKrSREz, QDKrSREG), (QDKrSREo, QDKrSREW)) == False:
                print('Cant find tail!')
            else:
                QDKrSREh = QDKrSREt.astar(QDKrSREP, (QDKrSREz, QDKrSREG), (QDKrSREo, QDKrSREW))
                if len(QDKrSREh) > 1:
                    QDKrSREa = QDKrSREh
                    print('Chasing tail!')
        QDKrSREP[QDKrSREo, QDKrSREW] = 1
        if QDKrSREa == [n for n in range(100)]:
            QDKrSREa = []
        if QDKrSREa == []:
            for QDKrSREI in QDKrSREl:
                for QDKrSREu in QDKrSREw:
                    QDKrSREq = QDKrSREt.astar(QDKrSREP, (QDKrSREz, QDKrSREG), (QDKrSREu, QDKrSREI))
                    if QDKrSREq != False and QDKrSREq != []:
                        print('found')
                        if len(QDKrSREq) > len(QDKrSREa):
                            QDKrSREa = QDKrSREq
                            print('PATH:', QDKrSREa)
        for QDKrSREf, snake in enumerate(game.snakes):
            if not snake.body:
                continue
            if QDKrSREf == snake_idx:
                continue
            else:
                QDKrSREt.last_enemy_head_coord_x = QDKrSREF
                QDKrSREt.last_enemy_head_coord_y = QDKrSREL
        if QDKrSREa != []:
            QDKrSRtE = QDKrSREa[-1]
            QDKrSRtC = QDKrSRtE[0]
            QDKrSRte = QDKrSRtE[1]
            QDKrSREe = QDKrSREt.calculate_direction(QDKrSRtC, QDKrSRte, QDKrSREz, QDKrSREG)
        else:
            print()
            print('DEAD!')
            print()
        return QDKrSREe

    def get_name(QDKrSREt, snake_idx: int):
        return 'Finn Agent'

    def heuristic(QDKrSREt, a, b):
        return abs(b[0] - a[0]) + abs(b[1] - a[1])

    def astar(QDKrSREt, array, start, goal):
        QDKrSRtf = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        QDKrSRtM = set()
        QDKrSRtn = {}
        QDKrSRtF = {start: 0}
        QDKrSRtL = {start: QDKrSREt.heuristic(start, goal)}
        QDKrSRtm = []
        heappush(QDKrSRtm, (QDKrSRtL[start], start))
        while QDKrSRtm:
            QDKrSRtz = heappop(QDKrSRtm)[1]
            if QDKrSRtz == goal:
                QDKrSRtG = []
                while QDKrSRtz in QDKrSRtn:
                    QDKrSRtG.append(QDKrSRtz)
                    QDKrSRtz = QDKrSRtn[QDKrSRtz]
                return QDKrSRtG
            QDKrSRtM.add(QDKrSRtz)
            for i, j in QDKrSRtf:
                QDKrSRto = QDKrSRtz[0] + i, QDKrSRtz[1] + j
                QDKrSRtW = QDKrSRtF[QDKrSRtz] + QDKrSREt.heuristic(QDKrSRtz, QDKrSRto)
                if 0 <= QDKrSRto[0] < array.shape[0]:
                    if 0 <= QDKrSRto[1] < array.shape[1]:
                        if array[QDKrSRto[0]][QDKrSRto[1]] == 1:
                            continue
                    else:
                        continue
                else:
                    continue
                if QDKrSRto in QDKrSRtM and QDKrSRtW >= QDKrSRtF.get(QDKrSRto, 0):
                    continue
                if QDKrSRtW < QDKrSRtF.get(QDKrSRto, 0) or QDKrSRto not in [i[1] for i in QDKrSRtm]:
                    QDKrSRtn[QDKrSRto] = QDKrSRtz
                    QDKrSRtF[QDKrSRto] = QDKrSRtW
                    QDKrSRtL[QDKrSRto] = QDKrSRtW + QDKrSREt.heuristic(QDKrSRto, goal)
                    heappush(QDKrSRtm, (QDKrSRtL[QDKrSRto], QDKrSRto))
        return False

    def calculate_direction(QDKrSREt, move_x, move_y, current_x, current_y):
        if move_y < current_y:
            QDKrSRtg = Direction.UP
            return QDKrSRtg
        else:
            if move_x < current_x:
                QDKrSRtg = Direction.LEFT
                return QDKrSRtg
            else:
                if move_y > current_y:
                    QDKrSRtg = Direction.DOWN
                    return QDKrSRtg
                else:
                    if move_x > current_x:
                        QDKrSRtg = Direction.RIGHT
                        return QDKrSRtg

    def calculate_next_move(QDKrSREt, move_x, move_y, current_x, current_y):
        if move_y < current_y:
            QDKrSRtU = move_y - 1
            return QDKrSRtU, move_x
        else:
            if move_x < current_x:
                QDKrSRts = move_x - 1
                return QDKrSRts, move_y
            else:
                if move_y > current_y:
                    QDKrSRtU = move_y + 1
                    return QDKrSRtU, move_x
                else:
                    if move_x > current_x:
                        QDKrSRts = move_x + 1
                        return QDKrSRts, move_y
# Created by pyminifier (https://github.com/liftoff/pyminifier)
