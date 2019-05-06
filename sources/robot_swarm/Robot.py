import argparse
import json
from time import sleep

import matplotlib.pyplot as plt
import requests
import random


class Robot:
    """
    Simulates the behaviour of a robot that is able to know its position and move to a given target.
    Movement is based on a 2D grid and the robot moves only to contiguous position (North, South, East, West)
    without diagonals.

    Robot is also able to communicate with other robots to coordinate movements and target positions through
    its associated miner. It knows about its miner from its IP address and port.
    """

    def __init__(self, peer_address="", miner_address="http://127.0.0.1:10000", id_robot=random.randint(1, 1001),
                 pos_x=0, pos_y=0):
        self.miner_address = miner_address
        self.position = [pos_x, pos_y]  #: Position of the robot in the grid.
        self.target = [0, 0]  #: Position to reach.
        self.id_robot = id_robot  #: Robot instance id.
        self.path = []  #: Path to follow from current position to reach target.
        self.peer_address = peer_address

    def register_me(self):
        headers = {'Content-Type': "application/json"}
        peer_info = {"peer": self.peer_address}
        requests.post(self.miner_address + "/register_peer", data=json.dumps(peer_info), headers=headers)
        requests.post(self.miner_address + "/register_me", headers=headers)

    def set_target(self, to_x, to_y):
        """
        Sets the target position. It updates the path to reach this new target.

        @param to_x: X axis position to reach
        @param to_y: Y axis position to reach
        """
        self.target = [to_x, to_y]
        self.set_path()

    def set_path(self):
        """
        It calculates the path from the current position to reach target and stores it in L{self.path} attribute.
        Path is an ordered list of cells the robot is going through. A cell is a two integers list where the first
        one is the X position and the second one is Y position.
        """
        self.path = []
        x0, y0 = self.position[0], self.position[1]  # Initial point
        x1, y1 = self.target[0], self.target[1]  # Target point

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

    def move_to_target(self, speed=1):
        """
        It changes current position of robot to the +I{speed} position in path and update path.
        :param speed: Number of positions in the move.
        :return: Nothing
        """

        """
        It changes current position of robot to the +I{speed} position in path and update path.

        @param speed: Number of positions in the move.
        """
        if not self.path:
            return False
        else:
            if speed < len(self.path):
                self.position = self.path[speed]
            else:
                self.position = self.path.pop()

            self.set_path()

    def add_new_transaction(self):
        """
        It adds a new transaction with its current position as data to its miner.

        @return: True, if request was successfully accomplished. False, otherwise.
        """
        tx_data = '{"id_robot": "' + str(self.id_robot) + '", "pos": ' + json.dumps(self.position) + '}'
        url = self.miner_address + "/add_new_transaction"
        headers = {'Content-Type': "application/json"}
        req = requests.post(url, data=tx_data, headers=headers)
        return req.ok

    def plot_path(self):
        """
        A test method that plots robot choosen path from its position to target.

        @return:
        """
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

    def print_info(self):
        """
        A test method that prints information about the state of the robot.

        @return:
        """
        print(80 * "-")
        print("Robot ID: " + str(self.id_robot))
        print("     Current Position: " + str(self.position))
        print("     Current Target  : " + str(self.target))
        path_to_print = ("\n" + 23 * " ").join((str(self.path))[i:i + 57] for i in range(0, len(str(self.path)), 57))
        print("     Following Path  : " + path_to_print)
        print(80 * "-")

    def start(self):
        """
        The Robot starts to do whatever it has to do.
        @return:
        """
        # First, if I know a peer, I register my self into the network.
        if self.peer_address:
            self.register_me()

        # For testing purpose, a target is going to be set to the robot.
        # Every N seconds, robot will move towards target. Speed will be the number
        # of steps made in the movement, it is the number of positions walked.
        # Then, it recalculates the path and moves again till target is reached.
        self.set_target(20, 25)

        self.print_info()
        self.add_new_transaction()
        requests.get(self.miner_address + "/mine")

        while len(self.path) > 1:
            i = random.randint(1, 10)
            print("Speed: " + str(i), end="      ")
            self.move_to_target(i)
            print("Positions to target: " + str(len(self.path)))
            self.print_info()
            self.add_new_transaction()
            requests.get(self.miner_address + "/mine")

        sleep(1000)


##################
# Robot Launcher #
##################
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Robot launcher.")
    parser.add_argument("miner_address", help="Miner address for this robot (like http://example.com:9090).")
    parser.add_argument("-p", "--peer_address", help="Address to a known existing peer.", default="")
    parser.add_argument("-i", "--id_robot", help="An integer for the Robot's ID.", type=int,
                        default=random.randint(1, 1001))
    args = parser.parse_args()

    robot = Robot(miner_address=args.miner_address)

    if args.peer_address:
        robot.peer_address = args.peer_address
    if args.id_robot:
        robot.id_robot = args.id_robot

    robot.start()
