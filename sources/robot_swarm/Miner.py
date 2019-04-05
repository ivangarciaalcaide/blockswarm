import json
import socket
import argparse
import requests
from flask import Flask, request, Response

from bs_blockchain.Blockchain import Blockchain
from bs_blockchain.Transaction import Transaction

app = Flask(__name__)


class Miner(Blockchain):

    def __init__(self):
        super().__init__()
        self.peers = []  #: List of connected peers by connection address.
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        self.connect_address = "http://" + s.getsockname()[0] + ":" + str(port)
        s.close()

    def select_transactions_to_mine(self):
        """
        In L{miner} all remaining unconfirmed transactions are selected.

        @return: Every unconfirmed transaction.
        """
        return self.unconfirmed_transactions.copy()


@app.route('/add_new_transaction/<spread>', methods=['POST'])
def add_new_transaction(spread):
    # Generate Transaction object from JSON and insert it into its miner unconfirmed transaction list.
    tx_json = request.get_json()
    if 'id_tx' in tx_json:
        tx = Transaction(json.dumps(tx_json.get('data')), id_tx=tx_json.get('id_tx'))
    else:
        tx = Transaction(json.dumps(tx_json))
    miner.add_new_transaction(tx)
    tx_json = json.loads(str(tx))

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


@app.route('/get_chain')
def get_chain():
    result = str(miner)
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


@app.route('/get_peers', methods=['POST', 'GET'])
def get_peers():
    # return json.dumps(miner.peers)
    return Response(json.dumps(miner.peers), status=200, content_type='application/json')


@app.route('/register_me', methods=['POST'])
def register_me():
    """
    Announce this miner to the rest of miners. This way, this new robot get peered with the rest.
    """

    # Requests to the known peer its set of peers so all of them got stored in the
    # list of known peers.
    headers = {'Content-Type': "application/json"}
    req = requests.post(miner.peers[0] + "/get_peers", headers=headers)
    if req.json():
        miner.peers.extend(req.json())

    # Tells to every known node to register me.
    my_info = {"peer": miner.connect_address}
    for peer in miner.peers:
        peer_url = str(peer) + "/register_peer"
        requests.post(peer_url, data=json.dumps(my_info), headers=headers)

    return "Success", 201


@app.route('/register_peer', methods=['POST'])
def register_peer():
    """
    Includes a new node to the list of peers.
    """
    peer_json = request.get_json()
    miner.peers.append(peer_json['peer'])
    return "Success", 201


##################
# Miner Launcher #
##################

parser = argparse.ArgumentParser(description="Miner launcher.")
parser.add_argument("port", help="port to bind (from 1024 to 65535).", type=int)
args = parser.parse_args()

# Collects arguments and create miner setting it appropriately.
port = int(args.port)
miner = Miner()

if port in range(1024, 65536):
    if __name__ == '__main__':
        # Flask is ready to get up so, some extra info is printed (like external ip address).
        print_separator = (len(miner.connect_address) + 19) * "-"
        print("\n" + print_separator)
        print("* My IP address: " + miner.connect_address + " *")
        print(print_separator + "\n")
        app.run('0.0.0.0', port)
    else:
        print("Not running as main application. Server won't go up.")
else:
    print("Port must be between 1024 and 65535.")
