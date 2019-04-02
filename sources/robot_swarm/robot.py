import matplotlib.pyplot as plt


class Robot:
    """
    Simulates the behaviour of a robot that is able to know its position and move to a given target.
    Movement is based on a 2D grid and the robot moves only to contiguous position (North, South, East, West)
    without diagonals.

    Robot is also able to communicate with other robots to coordinate movements and target positions through
    its associated miner. It knows about its miner from its IP address and port.
    """

    def __init__(self, miner_host="127.0.0.1", miner_port="10000", pos_x=0, pos_y=0):
        Robot.miner_host = miner_host   #: Associated miner IP.
        Robot.miner_port = miner_port   #: Associated miner port.
        self.position = [pos_x, pos_y]  #: Position of the robot in the grid.
        self.target = [0, 0]            #: Position to reach.
        self.path = []                  #: Path to follow from current position to reach target.

    def set_target(self, to_x, to_y):
        """
        Sets the target position.

        @param to_x: X axis position to reach
        @param to_y: Y axis position to reach
        """
        self.target = [to_x, to_y]

    def set_path(self):
        """
        It calculates the path from the current position to reach target and stores it in L{self.path} attribute.
        Path is an ordered list of cells the robot is going through. A cell is a two integers list where the first
        one is the X position and the second one is Y position.
        """
        x0, y0 = self.position[0], self.position[1]      # Initial point
        x1, y1 = self.target[0], self.target[1]          # Target point

        x_dist = abs(x1 - x0)
        y_dist = -abs(y1 - y0)

        x_step = 1 if x0 < x1 else -1
        y_step = 1 if y0 < y1 else -1

        error = x_dist + y_dist

        self.path.append([x0, y0])

        while x0 != x1 or y0 != y1:
            if 2 * error - y_dist > x_dist - 2 * error:
                error += y_dist
                x0 += x_step
            else:
                error += x_dist
                y0 += y_step

            self.path.append([x0, y0])

    def testing(self):
        print(self.path)

        plt.xlim(-10, 10)
        plt.ylim(-10, 10)
        plt.grid(True)
        plt.scatter(0, 0, marker="+")
        plt.scatter(*zip(*self.path))
        plt.plot(*zip(*self.path))

        l1, l2 = [self.position[0], self.target[0]], [self.position[1], self.target[1]]
        plt.plot(l1, l2, marker='o')
        plt.show()


robot = Robot(pos_x=-10, pos_y=10)
robot.set_target(10, -10)
robot.set_path()
print(str("(" + str(robot.position[0]) + ", " + str(robot.position[1]) + ")"), end=" ---> ")
print(str("(" + str(robot.target[0]) + ", " + str(robot.target[1]) + ")"))
robot.testing()



