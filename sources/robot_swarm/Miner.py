import json
import socket
import argparse

from flask import Flask, request

from bs_blockchain.Blockchain import Blockchain
from bs_blockchain.Transaction import Transaction

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


miner = Miner()


@app.route('/test/<test>')
def test(test):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return "TX:<br><br> " + test + "<br>" + str(miner.chain) + "<br>" + ip


@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    tx = Transaction(json.dumps(request.get_json()))
    miner.add_new_transaction(tx)
    return "Success", 201


@app.route('/show_pending_transactions')
def show_pending_transactions():
    result = json.dumps(miner.unconfirmed_transactions)
    return result


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


@app.route('/shutdown')
def shutdown():
    shutdown_server()
    return 'Server shutting down...'


parser = argparse.ArgumentParser()
parser.add_argument("port", help="port to bind (from 1024 to 65535).", type=int)
args = parser.parse_args()
port = int(args.port)

if port in range(1024, 65536):
    if __name__ == '__main__':
        app.run('0.0.0.0', port)
    else:
        print("Not running as main application. Server won't go up.")
else:
    print("Port must be between 1024 and 65535.")


