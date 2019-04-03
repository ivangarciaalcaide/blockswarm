import json
import socket
import argparse

import requests
from flask import Flask, request

from bs_blockchain.Blockchain import Blockchain
from bs_blockchain.Transaction import Transaction

app = Flask(__name__)


class Miner(Blockchain):

    def __init__(self):
        super().__init__()
        self.peers = []  #: List of connected peers by connection address.

    def select_transactions_to_mine(self):
        """
        In L{miner} all remaining unconfirmed transactions are selected.

        @return: Every unconfirmed transaction.
        """
        return self.unconfirmed_transactions.copy()


@app.route('/test/<test>')
def test(test):
    """
    # TODO: Remove this method as it is only for testing purpose.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return "TX:<br><br> " + test + "<br>" + str(miner.chain) + "<br>" + ip


@app.route('/add_new_transaction/<spread>', methods=['POST'])
def add_new_transaction(spread):
    # Generate Transaction object from JSON and insert it into its miner unconfirmed transaction list.
    tx_json = request.get_json()
    tx = Transaction(json.dumps(tx_json))
    miner.add_new_transaction(tx)

    # If it is the first peer to receive the TX, spread it to other peers.
    if spread == "do_spread":
        for peer in miner.peers:
            url = peer + "/add_new_transaction/no_spread"
            headers = {'Content-Type': "application/json"}
            requests.post(url, data=json.dumps(tx_json), headers=headers)

    return "Success", 201


@app.route('/get_pending_transactions')
def get_pending_transactions():
    result = json.dumps(miner.unconfirmed_transactions)
    return result


def shutdown_server():
    # TODO: This is a totally unsafe way of shutting down server.
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


@app.route('/shutdown')
def shutdown():
    """
    Shutdowns Miner. It means, stop web service and terminate process.
    @return: Warning string.
    """
    shutdown_server()
    return 'Server shutting down...'


"""
Module execution starts here...
"""

parser = argparse.ArgumentParser(description="Miner launcher.")
parser.add_argument("port", help="port to bind (from 1024 to 65535).", type=int)
parser.add_argument("-p", "--peer", help="Address to a known existing peer (like http://example.com:9090", default="")
args = parser.parse_args()

# Collects arguments and create miner setting it appropriately.
port = int(args.port)
miner = Miner()
if args.peer:
    miner.peers.append(args.peer)
    print("PEERS: " + str(miner.peers))

if port in range(1024, 65536):
    if __name__ == '__main__':
        # Flask is ready to get up so, some extra info is printed (like external ip address).
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        print(40 * "-")
        print(" * My IP address: " + s.getsockname()[0])
        print(40 * "-" + "")
        s.close()
        app.run('0.0.0.0', port)
    else:
        print("Not running as main application. Server won't go up.")
else:
    print("Port must be between 1024 and 65535.")
