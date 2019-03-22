import json
import time
from abc import abstractmethod

from bs_blockchain.Block import Block


class Blockchain:

    def __init__(self):
        self.unconfirmed_transactions = []  #: Set of transactions wating to be mined.
        self.chain = []  #: List og blocks that conforms the block chain
        self.pow_difficulty = 4  #: Difficulty of PoW
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

    def proof_of_work(self, block):
        """
        Proof of work implementation.

        It takes a block and sets its nonce to 0. Then, calculates its hash from
        L{Block.get_string_to_hash(self)<Block.get_string_to_hash(self)>}. This hash must
        end with, at least, as many '0's characters as indicated in
        L{pow_difficulty} to success. I hash doesn't accomplish PoW, nonce value is
        incremented by 1 and it starts over.

        Once nonce is found, block's hash is updated.

        @param block: Block over the proof of work is executed.
        # @return: String with the hash that accomplish the PoW.
        """
        block.nonce = 0
        current_hash = block.calculate_hash()
        while not current_hash.endswith('0' * self.pow_difficulty):
            block.nonce += 1
            current_hash = block.calculate_hash()

        block.hash = current_hash

    # def is_valid_proof(self, block):

    def add_new_transaction(self, transaction):
        """
        Insert a L{Transaction} at the end of L{unconfirmed transactions<unconfirmed_transactions>}
        list.

        @param transaction: L{Transaction} object to be inserted.
        """
        self.unconfirmed_transactions.append(json.loads(transaction.__str__()))

    @abstractmethod
    def select_transactions_to_mine(self):
        """
        It selects what transactions to be mined in a given block.

        @return: A list with selected L{transactions<Transaction>}
        """

    def mine(self, allow_empty_transactions=False):
        """
        Mines a new block and add it to the chain.

        Mining steps:
            1. Selects transactions to be incorporated to the block.
            2. Creates a block with current information available
                - Selected transactions
                - Current time for timestamp
                - Previous hash filled with last block hash.
            3. Fills hash field with proof of work.
            4. Removes mined transactions from L{unconfirmed_transactions} list.


        @type allow_empty_transactions: boolean
        @param allow_empty_transactions: True, mine the block even if transaction's block list is empty.

        @return: False, If block could not be mined. The mined block, otherwise.
        """
        selected_transactions = self.select_transactions_to_mine()
        if not selected_transactions and not allow_empty_transactions:
            return False

        last_block = self.last_block

        new_block = Block(
            index=last_block.index + 1,
            transactions=selected_transactions,
            timestamp=time.time(),
            previous_hash=last_block.hash)

        self.proof_of_work(new_block)
        result = self.add_block(new_block)
        if result:
            for element in new_block.transactions:
                if element in self.unconfirmed_transactions:
                    self.unconfirmed_transactions.remove(element)

        return result

    def is_valid_block(self, block):
        """
        Checks if the block is a valid one.

        To be a valid block it has to accomplish following criteria:
            1. Its previous hash must be the same as previous block hash.
            2. Its index must be the following from previous block.
            3. Its hash must end with at least L{pow_difficulty} numbers of '0's
            4. Its hash must be the same than calculated hash.

        @param block: Block to be checked
        @return: False if not valid. True, otherwise.
        """
        if self.last_block.hash != block.previous_hash:
            return False

        if self.last_block.index != block.index - 1:
            return False

        if not block.hash.endswith('0' * self.pow_difficulty):
            return False

        if block.hash != block.calculate_hash():
            return False

        return True

    def add_block(self, new_block):
        """
        Append a new block to the chain after checking its correctness.

        @param new_block: New block to be added.
        @return: False, if block couldn't be added. The new block, otherwise.
        """
        if self.is_valid_block(new_block):
            self.chain.append(new_block)
            return new_block
        else:
            return False

    @property
    def last_block(self):
        """
        Reference to the last block of the chain.
        """
        return self.chain[-1]

    def __str__(self):
        result = ""
        for block in self.chain:
            result = result + block.__str__() + "\n"
        return result


class MyBlockChain(Blockchain):

    def __init__(self):
        super().__init__()

    def select_transactions_to_mine(self):
        """
        In L{MyBlockChain} all remaining unconfirmed transactions are selected.

        @return: Every unconfirmed transaction.
        """
        return self.unconfirmed_transactions.copy()
