import json
import socket
import argparse
import requests
from flask import Flask, request, Response

from bs_blockchain.Block import Block
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
        All remaining unconfirmed transactions are selected.

        :return: Every unconfirmed transaction.
        """
        return self.unconfirmed_transactions.copy()


def consensus():
    my_len = len(miner.chain)

    for peer in miner.peers:
        url = peer + "/get_chain_length"
        headers = {'Content-Type': "application/json"}
        his_len = int((requests.post(url, headers=headers)).json())

        if int(his_len) > my_len:
            miner.chain = []  # his_chain
            # TODO: Quitar traza
            print("La cadena de " + url + " es más larga")

            # blocks = requests.post(url, headers=headers)).json()

            # new_chain = []
            # for x in range(0, len(blocks)):
            #     new_chain.append(Block(0, [], 0, '0'))
            #     for key in blocks[x]:
            #         setattr(new_chain[x], key, blocks[x][key])


@app.route('/add_block', methods=['POST'])
def add_block():
    block_json = request.get_json()
    block = miner.add_block(Block(
        index=block_json["index"],
        hash_pre=block_json["hash"],
        transactions=block_json["transactions"],
        timestamp=block_json["timestamp"],
        previous_hash=block_json["previous_hash"],
        nonce=block_json["nonce"]))

    if block:
        # If new block is accepted, its txs are deleted from unconfirmed transactions.
        block_txs = []
        x = 0
        for tx in block.transactions:
            block_txs.append(Transaction(
                id_tx=tx["id_tx"],
                data=json.dumps(tx["data"])
            ))
            print("Block's (" + str(block.index) + ") TX_ID " + str(x) + ": " + str(block_txs[x].id_tx))
            x += 1

        for tx in block_txs:
            for tx_unconfirmed in miner.unconfirmed_transactions:
                if tx_unconfirmed['id_tx'] == tx.id_tx:
                    miner.unconfirmed_transactions.remove(tx_unconfirmed)
        return "Success", 200
    else:
        return "Not valid block", 401


@app.route('/mine', methods=['GET'])
def mine():
    # consensus()
    block = miner.mine()
    for peer in miner.peers:
        url = peer + "/add_block"
        headers = {'Content-Type': "application/json"}
        datos = str(block)
        requests.post(url, data=datos, headers=headers)

    return "Success", 200


@app.route('/get_chain_length', methods=['GET'])
def get_chain_length():
    result = json.dumps(str(len(miner.chain)))
    return Response(result, status=200, content_type='application/json')


@app.route('/add_new_transaction', methods=['POST'])
def add_new_transaction():
    """
    When a transaction is created by a process, it tells its miner to add the new transaction through calling
    this method. It will add the new transaction into :py:attr:Blockchain.unconfirmed_transactions: queue and will
    annouce it to the rest of peers for them to register it also.

    :return: "Success", 200
    """
    store_transaction(request.get_json())

    for peer in miner.peers:
        url = peer + "/register_transaction"
        headers = {'Content-Type': "application/json"}
        requests.post(url, data=json.dumps(request.get_json()), headers=headers)

    return "Success", 200


@app.route('/register_transaction', methods=['POST'])
def register_transaction():
    """
    Includes a new transaction to the list of py:attr:Blockchain.unconfirmed_transactions:.
    """
    store_transaction(request.get_json())

    return "Success", 200


def store_transaction(tx_json):
    # tx = Transaction(json.dumps(tx_json))
    if 'id_tx' in tx_json:
        tx = Transaction(json.dumps(tx_json.get('data')), id_tx=tx_json.get('id_tx'))
    else:
        tx = Transaction(json.dumps(tx_json))
    miner.add_new_transaction(tx)


@app.route('/get_pending_transactions', methods=['GET'])
def get_pending_transactions():
    """
    Returns a list of the :py:attr:Blockchain.unconfirmed_transactions: that are waiting to be mined.

    :return: List of transactions ready to be mined.
    """
    result = json.dumps(miner.unconfirmed_transactions, indent=4)
    return Response(result, status=200, content_type='application/json')


@app.route('/get_chain', methods=['GET'])
def get_chain():
    """
    Retruns the whole chain stored by the miner.

    :return: Chain of the miner.
    """
    return Response(str(miner), status=200, content_type='application/json')


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


@app.route('/get_peers', methods=['GET'])
def get_peers():
    """
    Returns the list of peers known by the miner.

    :return: List of miner's peers.
    """
    return Response(json.dumps(miner.peers), status=200, content_type='application/json')


@app.route('/register_me', methods=['POST'])
def register_me():
    """
    Announce this miner to the rest of miners. This way, this new process/miner get peered with the rest.

    :return: "Success", 200 or "Chain NOT valid !!!", 401
    """

    # Requests to the known peer its set of peers so all of them got stored in the
    # list of known peers.
    headers = {'Content-Type': "application/json"}
    req = requests.get(miner.peers[0] + "/get_peers", headers=headers)
    if req.json():
        miner.peers.extend(req.json())

    # As there is one peer at least that have created the chain, I'll accept his.
    # TODO Instead of requesting the chain of the first peer, it can be requested the longest chain or obtain it from
    #   whatever consensus is implemented.
    req = requests.get(miner.peers[0] + "/get_chain", headers=headers)
    blocks = req.json()['chain']
    new_chain = []
    for x in range(0, len(blocks)):
        new_chain.append(Block(0, [], 0, '0'))
        for key in blocks[x]:
            setattr(new_chain[x], key, blocks[x][key])

    if len(new_chain) == 1 or miner.is_valid_chain(new_chain):
        miner.chain = new_chain
    else:
        return "Chain NOT valid !!!", 401

    # We'll take its unconfirmed transactions too.
    req = requests.get(miner.peers[0] + "/get_pending_transactions", headers=headers)
    for tx in req.json():
        store_transaction(tx)

    # Tells to every known node to register me.
    my_info = {"peer": miner.connect_address}
    for peer in miner.peers:
        peer_url = str(peer) + "/register_peer"
        requests.post(peer_url, data=json.dumps(my_info), headers=headers)

    return "Success", 200


@app.route('/register_peer', methods=['POST'])
def register_peer():
    """
    Includes a new node to the list of peers.

    :return: "Success", 200
    """
    peer_json = request.get_json()
    miner.peers.append(peer_json['peer'])
    return "Success", 200


##################
# Miner Launcher #
##################

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Miner launcher.")
    parser.add_argument("port", help="port to bind (from 1024 to 65535).", type=int)
    args = parser.parse_args()

    # Collects arguments and create miner setting it appropriately.
    port = int(args.port)
    miner = Miner()

    if port in range(1024, 65536):
        # Flask is ready to get up so, some extra info is printed (like external ip address).
        print_separator = (len(miner.connect_address) + 19) * "-"
        print("\n" + print_separator)
        print("* My IP address: " + miner.connect_address + " *")
        print(print_separator + "\n")
        app.run('0.0.0.0', port, threaded=True)
    else:
        print("Port must be between 1024 and 65535.")
else:
    print("Not running as main application. Server won't go up.")
