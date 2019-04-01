from robot_swarm.Miner import Miner
import matplotlib.pyplot as plt


class Robot:

    def __init__(self, miner_host="127.0.0.1", miner_port="10000", pos_x=0, pos_y=0):
        Robot.miner_host = miner_host
        Robot.miner_port = miner_port
        miner = Miner()
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.to_x = 0
        self.to_y = 0

    def set_target(self, to_x, to_y):
        self.to_x = to_x
        self.to_y = to_y

    def move_to_target(self, speed):
        x1, y1 = self.pos_x, self.pos_y
        x2, y2 = self.to_x, self.to_y

        cont = 0
        points = []

        while (x1 != x2 or y1 != y2) and cont < 20:
            cont += 1
            a = y2 - y1
            b = x2 - x1
            c = a * x1 + b * y1

            y = (c - a * (x1 + 1)) / b

            if y > 0.5:
                x1 += 1
            else:
                y1 += 1

            points.append((x1, y1))
            print("(x1, y1) = (" + str(x1) + ", " + str(y1) + ") --- " + str(y))

        print(str(points))

        plt.xlim(0, 10)
        plt.ylim(0, 10)
        plt.scatter(*zip(*points))
        plt.plot(*zip(*points))

        l1, l2 = [0, 8], [0, 4]
        plt.plot(l1, l2, marker='o')
        plt.show()

    def move_to_target_2(self, speed):
        x1, y1 = self.pos_x, self.pos_y
        x2, y2 = self.to_x, self.to_y

        # hz = x2 - x1
        # vt = y2 - y1

        hz_step = (x2 - x1) // (y2 - y1)

        # print("(x1, y1) = (" + str(x1) + ", " + str(y1) + ") --- (" + str(hz) + ", " + str(vt) + ")" + " --- " + str(hz_step))
        print("(x1, y1) = (" + str(x1) + ", " + str(y1) + ") --- STEP: " + str(hz_step))
        points = []

        while y1 <= y2:
            points.append((x1, y1))
            for x in range(0, hz_step):
                x1 += 1
                if x1 <= x2:
                    points.append((x1, y1))
            y1 += 1

        while x1 < x2:
            x1 += 1
            points.append((x1, y2))

        print(str(points))

        plt.xlim(0, 10)
        plt.ylim(0, 10)
        plt.scatter(*zip(*points))
        plt.plot(*zip(*points))

        l1, l2 = [0, 8], [0, 4]
        plt.plot(l1, l2, marker='o')
        plt.show()

    def move_to_target_3(self, speed):
        points = []
        x0, y0 = self.pos_x, self.pos_y
        x1, y1 = self.to_x, self.to_y

        dx = x1 - x0
        dy = y1 - y0

        xsign = 1 if dx > 0 else -1
        ysign = 1 if dy > 0 else -1

        dx = abs(dx)
        dy = abs(dy)

        if dx > dy:
            xx, xy, yx, yy = xsign, 0, 0, ysign
        else:
            dx, dy = dy, dx
            xx, xy, yx, yy = 0, ysign, xsign, 0

        D = 2 * dy - dx
        y = 0

        for x in range(dx + 1):
            points.append((x0 + x * xx + y * yx, y0 + x * xy + y * yy))
            if D >= 0:
                y += 1
                D -= 2 * dx
            D += 2 * dy

        return points

    def testing(self, speed):
        points = self.move_to_target_3(2)
        print(str(points))

        plt.xlim(0, 10)
        plt.ylim(0, 10)
        plt.scatter(*zip(*points))
        plt.plot(*zip(*points))

        l1, l2 = [0, 8], [0, 4]
        plt.plot(l1, l2, marker='o')
        plt.show()

robot = Robot(pos_x=0, pos_y=0)
robot.set_target(8, 4)
print(str("(" + str(robot.pos_x) + ", " + str(robot.pos_y) + ")"), end=" ---> ")
print(str("(" + str(robot.to_x) + ", " + str(robot.to_y) + ")"))
robot.move_to_target(2)



