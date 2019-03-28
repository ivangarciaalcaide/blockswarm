from robot_swarm.Miner import Miner


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

            print("(x1, y1) = (" + str(x1) + ", " + str(y1) + ") --- " + str(y))


robot = Robot(pos_x=0, pos_y=0)
robot.set_target(15, 5)
print(str("(" + str(robot.pos_x) + ", " + str(robot.pos_y) + ")"), end=" ---> ")
print(str("(" + str(robot.to_x) + ", " + str(robot.to_y) + ")"))
robot.move_to_target(2)



