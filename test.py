from bs_blockchain.Blockchain import MyBlockChain
from bs_blockchain.Transaction import Transaction

print("Testing...")

blockchain = MyBlockChain()

print("-----")
#tx1 = Transaction({"SALUDO": "Hola"})
#tx2 = Transaction({"SALUDO": "Adios"})
#tx3 = Transaction({"Nombre": "Pepe"})

# tx1 = Transaction("Hola")
# tx2 = Transaction("Adios")
# tx3 = Transaction("Pepe")
#
# blockchain.add_new_transaction(tx1)
# blockchain.add_new_transaction(tx2)
# blockchain.add_new_transaction(tx3)
# blockchain.mine()
# tx4 = Transaction("Valde")
# tx5 = Transaction("Rama")
# blockchain.add_new_transaction(tx4)
# blockchain.add_new_transaction(tx5)
# blockchain.mine()

tx6 = Transaction('{"increase": "combine","summer": -779209931}')
blockchain.add_new_transaction(tx6)
tx7 = Transaction('{"ourselves":"wait","stranger":1805843303,"than":"still","certain":false,"entire":"dirt"}')
blockchain.add_new_transaction(tx7)
blockchain.mine()
tx8 = Transaction('["answer",false,"garden",false,true]')
blockchain.add_new_transaction(tx8)
blockchain.mine()

print(blockchain)
print("Unconfirmed transactions (" + str(len(blockchain.unconfirmed_transactions)) + "): " + str(blockchain.unconfirmed_transactions))

#blockchain.chain[2].previous_hash = "holamariposa"
check = blockchain.is_valid_chain(blockchain.chain)
print(check)
# print(blockchain)
# print("Unconfirmed transactions (" + str(len(blockchain.unconfirmed_transactions)) + "): " + str(blockchain.unconfirmed_transactions))