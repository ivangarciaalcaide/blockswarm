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

        xDist = abs(x1 - x0)
        yDist = -abs(y1 - y0)

        xStep = 1 if x0 < x1 else -1
        yStep = 1 if y0 < y1 else -1

        error = xDist + yDist

        points.append((x0, y0))

        while x0 != x1 or y0 != y1:
            if 2 * error - yDist > xDist - 2 * error:
                error += yDist
                x0 += xStep
            else:
                error += xDist
                y0 += yStep

            points.append((x0, y0))

        return points

    def testing(self, speed):
        points = self.move_to_target_3(2)
        print(str(points))

        plt.xlim(-20, 10)
        plt.ylim(-20, 10)
        plt.scatter(*zip(*points))
        plt.plot(*zip(*points))

        l1, l2 = [0, -16], [0, 3]
        plt.plot(l1, l2, marker='o')
        plt.show()

robot = Robot(pos_x=0, pos_y=0)
robot.set_target(-16, 3)
print(str("(" + str(robot.pos_x) + ", " + str(robot.pos_y) + ")"), end=" ---> ")
print(str("(" + str(robot.to_x) + ", " + str(robot.to_y) + ")"))
robot.testing(2)



