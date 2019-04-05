import sys
from robot_swarm.Robot import Robot

print("\n----------")
print("Testing...")
print("----------")

robots = [
    Robot(miner_address="http://127.0.0.1:10000", id_robot=1, pos_x=1, pos_y=1),
    Robot(peer_address="http://127.0.0.1:10000", miner_address="http://127.0.0.1:20000", id_robot=2, pos_x=2, pos_y=2),
    Robot(peer_address="http://127.0.0.1:20000", miner_address="http://127.0.0.1:30000", id_robot=3, pos_x=3, pos_y=3),
    Robot(peer_address="http://127.0.0.1:20000", miner_address="http://127.0.0.1:40000", id_robot=4, pos_x=4, pos_y=4)
]

robots[0].start()

sys.exit()

# parser = argparse.ArgumentParser(description="Test launcher.")
# parser.add_argument("port", help="port to bind (from 1024 to 65535).", type=int)
# args = parser.parse_args()
#
# # Collects arguments and create miner setting it appropriately.
# port = int(args.port)
#
# robot = Robot(pos_x=-10, pos_y=10)
# robot.set_target(10, -10)
# robot.set_path()
# print(str("(" + str(robot.position[0]) + ", " + str(robot.position[1]) + ")"), end=" ---> ")
# print(str("(" + str(robot.target[0]) + ", " + str(robot.target[1]) + ")"))
# # robot.plot_path()
#
# # robot.add_new_transaction()
# # robot.position = [5, 5]
# # sleep(1)
# # robot.add_new_transaction()
# sleep(5)
# url = robot.miner_address + "/shutdown"
# print(requests.get(url).text)
# print(requests.get("http://127.0.0.1:11000/shutdown").text)
# print(requests.get("http://127.0.0.1:9000/shutdown").text)
#


# tx1 = Transaction({"SALUDO": "Hola"})
# tx2 = Transaction({"SALUDO": "Adios"})
# tx3 = Transaction({"Nombre": "Pepe"})

# tx1 = Transaction("Hola")
# tx2 = Transaction("Adios")
# tx3 = Transaction("Pepe")
#
# blockchain.add_new_transaction(tx1)
# blockchain.add_new_transaction(tx2)
# blockchain.add_new_transaction(tx3)
# blockchain.mine()
# tx4 = Transaction("Valde")
# tx5 = Transaction("Rama")
# blockchain.add_new_transaction(tx4)
# blockchain.add_new_transaction(tx5)
# blockchain.mine()


# for x in range(2000):
#     if x % 100 == 0:
#         print(str(x))
#     tx6 = Transaction('{"increase": "combine","summer": -779209931}')
#     tx7 = Transaction('{"ourselves":"wait","stranger":1805843303,"than":"still","certain":false,"entire":"dirt"}')
#     blockchain.add_new_transaction(tx6)
#     blockchain.add_new_transaction(tx7)
#     blockchain.mine()
#
#     tx8 = Transaction('[{"forty":true,"physical":false},-1952659469.9578228]')
#     blockchain.add_new_transaction(tx8)
#     blockchain.mine()
#
#     tx9 = Transaction('{"important":"enjoy","smell":[false,"difficult"]}')
#     blockchain.add_new_transaction(tx9)
#     blockchain.mine()

# chain_id = blockchain.chain
# print("-------------------------------------------")
# print("Current blockchain from mining")
# print(blockchain)
# print("Is a valid chain? : " + str(blockchain.is_valid_chain(blockchain.chain)))
# print("-------------------------------------------")
# print("Saving chain to file...")
# blockchain.chain_to_file("chain_1.txt.gz", 9)
# blockchain.chain_to_file("chain_2.txt.gz", 1)
# blockchain.chain_to_file("chain_3.txt", 0)
# print("File saved.")
# print("-------------------------------------------")
# tx10 = '{"forward":[-1907593984.0836291,false],"quietly":"certain"}'
# print("Adding tx: " + tx10)
# blockchain.add_new_transaction(tx10)
# blockchain.mine()
# print("Transaction added.")
# print("-------------------------------------------")
# print("Current blockchain from mining")
# print(blockchain)
# print("Is valid chain? : " + str(blockchain.is_valid_chain(blockchain.chain)))
# print("-------------------------------------------")
# print("Updating blockchain from file.")
# blockchain.chain_from_file("chain_3.txt")
# print("Updated.")
# print("-------------------------------------------")
# print("Current blockchain from mining. Last transaction should not appear.")
# print(blockchain.chain[90])
# print("Is a valid chain? : " + str(blockchain.is_valid_chain(blockchain.chain)))
# print("-------------------------------------------")

# print("Previous chain: " + str(chain_id))
# print("Current chain : " + str(blockchain.chain))

# print("Current chain length: " + str(len(blockchain.chain)))

# print("Unconfirmed transactions (" + str(len(blockchain.unconfirmed_transactions)) + "): " + str(blockchain.unconfirmed_transactions))

# blockchain.chain[2].previous_hash = "holamariposa"
# check = blockchain.is_valid_chain(blockchain.chain)
# print(check)


# print(blockchain)
# print(blockchain.is_valid_chain(blockchain.chain))
# print(blockchain.chain[1].timestamp)
# print("Unconfirmed transactions (" + str(len(blockchain.unconfirmed_transactions)) + "): " + str(blockchain.unconfirmed_transactions))
