import sys

sys.path.insert(0, '/home/ivan/Workspace/PyCharm/blockswarm/sources')

from bs_blockchain.Blockchain import Blockchain
from bs_blockchain.Transaction import Transaction
from flask import Flask, request
import json
import socket

app = Flask(__name__)


class Miner(Blockchain):

    def __init__(self):
        super().__init__()
        self.peers = ()

    def select_transactions_to_mine(self):
        """
        In L{miner} all remaining unconfirmed transactions are selected.

        @return: Every unconfirmed transaction.
        """
        return self.unconfirmed_transactions.copy()


# @app.route('/add_transaction', methods=['POST'])
# def add_transaction():
#     tx = Transaction(json.dumps(request.get_json()))
#     miner.add_new_transaction(tx)
#     # tx1 = Transaction({"SALUDO": "Hola"})
#     return "Success", 201


miner = Miner()


@app.route('/test/<test>')
def test(test):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return "TX:<br><br> " + test + "<br>" + str(miner.chain) + "<br>" + ip


@app.route('/new_transaction', methods=['POST'])
def new_transaction():
    tx_data = request.get_json()
    miner.add_new_transaction(tx_data)

    return "Success", 201


if __name__ == '__main__':
    app.run('0.0.0.0', 10000)
