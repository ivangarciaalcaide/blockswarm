from hashlib import sha256
import json


class Block:

    def __init__(self, index, transactions, timestamp, previous_hash, nonce=0):
        self.index = index  #: Position number in the chain (starting from 0).
        self.hash = 0  #: Hash of this block.
        self.transactions = transactions  #: List of transactions in the block.
        self.timestamp = timestamp  #: Block creation time.
        self.previous_hash = previous_hash  #: Hash of previous block in the chain.
        self.nonce = nonce  #: Magic number to get the proof of work.

    def calculate_hash(self):
        """
        Calculates the block hash.

        It dumps it's fields values (state of the object) into an String and gets
        the sha256 of it. The own hash is not included in this operation.

        @return: String representing the hash.
        """
        return sha256(self.get_string_to_hash().encode()).hexdigest()

    def get_string_to_hash(self):
        """
        Forms the string from the state of the object to be hashed. It is a list of
        all attributes and their current value except block's own hash.

        @return: The string to be hashed.
        """
        my_json = json.loads(json.dumps(self.__dict__))

        if 'hash' in my_json:
            del my_json['hash']

        my_string = json.dumps(my_json, sort_keys=True)

        return my_string

    def __str__(self):
        return json.dumps(self.__dict__, indent=4, sort_keys=True)
