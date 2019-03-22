import time
from bs_blockchain.Block import Block


class Blockchain:

    def __init__(self):
        self.unconfirmed_transactions = []  # Set of transactions wating to be mined.
        self.chain = []  # List og blocks that conforms the block chain
        self.create_genesis_block()

    def create_genesis_block(self):
        """
        Creates first block of the chain and append it to the chain.

        Considerations:
            - It is indexed at position 0.
            - As there is not a previous block, previous_hash is set to "0".
            - As there are not transactions to mine yet, transaction list is empty.
        """
        genesis_block = Block(0, [], time.time(), "0")
        genesis_block.hash = genesis_block.calculate_hash()
        self.chain.append(genesis_block)

    @property
    def last_block(self):
        return self.chain[-1]

    def __str__(self):
        result = ""
        for block in self.chain:
            result = result + block.__str__()
        return result



