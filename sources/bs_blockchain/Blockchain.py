from bs_blockchain.Block import Block
from abc import abstractmethod
import binascii
import json
import time
import gzip
import pickle


class Blockchain:

    def __init__(self):
        self.unconfirmed_transactions = []  #: Set of transactions wating to be mined.
        self.chain = []  #: List og blocks that conforms the block chain
        self.pow_difficulty = 0  #: Difficulty of PoW
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

    def add_new_transaction(self, transaction):
        """
        Insert a L{Transaction} at the end of L{unconfirmed transactions<unconfirmed_transactions>}
        list.

        @param transaction: L{Transaction} object to be inserted.
        """
        self.unconfirmed_transactions.append(json.loads(str(transaction)))

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

    def is_valid_block(self, block, chain=None):
        """
        Checks if the block is a valid one.

        To be a valid block it has to accomplish following criteria:
            1. Its previous hash must be the same as previous block hash.
            2. Its index must be the following from previous block.
            3. Its hash must end with at least L{pow_difficulty} numbers of '0's
            4. Its hash must be the same than calculated hash.

        @param chain: Chain where the block is. If empty, it takes its own chain.
        @param block: Block to be checked.
        @return: False if not valid. True, otherwise.
        """
        if chain is None:
            chain = []
        if not chain:
            chain = self.chain

        previous_block = chain[block.index - 1]

        if previous_block.hash != block.previous_hash:
            return False

        if previous_block.index != block.index - 1:
            return False

        if not block.hash.endswith('0' * self.pow_difficulty):
            return False

        if block.hash != block.calculate_hash():
            return False

        return True

    def is_valid_chain(self, chain):
        """
        It checks if every block in the chain L{is_valid_block}.

        @param chain: The chain to check
        @return: True, if it is valid. False, otherwise.
        """
        x = 1
        while x < len(chain) and self.is_valid_block(chain[x], chain):
            x += 1
        if x == len(chain) and self.is_valid_block(chain[x-1], chain):
            return True
        else:
            return False

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

    def chain_to_file(self, filename, compress_level=0):
        """
        Saves the current chain into a file.

        Depending on B{compress_level} it behaves in two different ways. B{compress_level} range is
        from 0 to 9. By default, B{compress_level} is set to 0:
            - "B{0}": No compress and JSON text file is generated I{UTF-8} encoded.
            - "B{1 - 9}": Compressed B{gzip} file is generated. B{1} is fastest and produces the least compression.
                            B{9} is slowest and produces the most compression. File will not be human readable.

        Working with text files is much harder and takes much longer than with binary (compressed) files.

        @type filename: String
        @param filename: Desired name for the file. (Path is relative to working dir)
        @type compress_level: int
        @param compress_level: Desired compress level or, 0, produces a JSON text file (UTF-8).
        """
        if compress_level in range(1, 10):
            with gzip.open(filename, "wb", compresslevel=compress_level) as gzip_file:
                pickle.dump(self.chain, gzip_file, protocol=-1)
        elif compress_level == 0:
            with open(filename, mode="w", encoding='utf-8') as json_file:
                json_file.write(self.__str__())
        else:
            return False

    def chain_from_file(self, filename):
        """
        Reads a file that contains a chain and store it as its chain if it is valid.

        @param filename: Name of the file wher the chain is stored. (Path is relative to working dir)
        """
        with open(filename, "rb") as checking_file:
            is_gzip_file = binascii.hexlify(checking_file.read(2)) == b'1f8b'

        if is_gzip_file:
            with gzip.open(filename, "rb") as gzip_file:
                new_chain = pickle.load(gzip_file)
        else:
            with open(filename, "r") as json_file:
                blocks = json.load(json_file)['chain']
                new_chain = []
                for x in range(0, len(blocks)):
                    new_chain.append(Block(0, [], 0, '0'))
                    for key in blocks[x]:
                        setattr(new_chain[x], key, blocks[x][key])

        if self.is_valid_chain(new_chain):
            self.chain = new_chain
            return True
        else:
            return False

    @property
    def last_block(self):
        """
        Reference to the last block of the chain.
        """
        return self.chain[-1]

    def __str__(self):
        result = '{"chain" : ['
        for block in self.chain:
            result = result + block.__str__() + ",\n"
        result = result[0:-2]
        result += "]}"
        mi_json = json.loads(result)
        return json.dumps(mi_json, indent=4)


# class MyBlockChain(Blockchain):
#
#     def __init__(self):
#         super().__init__()
#
#     def select_transactions_to_mine(self):
#         """
#         In L{MyBlockChain} all remaining unconfirmed transactions are selected.
#
#         @return: Every unconfirmed transaction.
#         """
#         return self.unconfirmed_transactions.copy()
