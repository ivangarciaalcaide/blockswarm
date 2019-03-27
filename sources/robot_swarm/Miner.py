import sys

sys.path.insert(0, '/home/ivan/Workspace/PyCharm/blockswarm/sources')

from bs_blockchain.Blockchain import Blockchain
from bs_blockchain.Transaction import Transaction
from flask import Flask, request
import json


class Miner(Blockchain):

    def __init__(self):
        super().__init__()

    def select_transactions_to_mine(self):
        """
        In L{miner} all remaining unconfirmed transactions are selected.

        @return: Every unconfirmed transaction.
        """
        return self.unconfirmed_transactions.copy()


miner = Miner()
app = Flask(__name__)


@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    tx = Transaction(json.dumps(request.get_json()))
    miner.add_new_transaction(tx)
    # tx1 = Transaction({"SALUDO": "Hola"})
    return "Success", 201


@app.route('/test')
def test():
    return str(miner.unconfirmed_transactions)


if __name__ == '__main__':
    app.run('0.0.0.0', 10000)

