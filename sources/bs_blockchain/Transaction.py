import json
import time
from hashlib import sha1


class Transaction:

    # TODO: Generated unique id is not unique as different Transaction objects could be hashed the same.
    #  Is that a problem?
    def __init__(self, data):
        self.id = sha1((json.dumps(data) + str(time.time())).encode()).hexdigest()  #: Generated unique Id
        self.data = json.loads(data)  #: Custom data for transaction in B{json} format

    def __str__(self):
        return json.dumps(self.__dict__)
