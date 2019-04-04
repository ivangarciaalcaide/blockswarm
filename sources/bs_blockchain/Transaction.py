import json
import time
from hashlib import sha1


class Transaction:

    # TODO: Generated unique id is not unique as different Transaction objects could be hashed the same.
    #  Is that a problem?
    def __init__(self, data, id_tx=""):
        if not id_tx:
            self.id_tx = sha1((json.dumps(data) + str(time.time())).encode()).hexdigest()  #: Generated unique Id
        else:
            self.id_tx = id_tx

        self.data = json.loads(data)  #: Custom data for transaction in B{json} format

    def __str__(self):
        return json.dumps(self.__dict__)
