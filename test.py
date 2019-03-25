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
tx7 = Transaction('{"ourselves":"wait","stranger":1805843303,"than":"still","certain":false,"entire":"dirt"}')
blockchain.add_new_transaction(tx6)
blockchain.add_new_transaction(tx7)
blockchain.mine()

tx8 = Transaction('[{"forty":true,"physical":false},-1952659469.9578228]')
blockchain.add_new_transaction(tx8)
blockchain.mine()

tx9 = Transaction('{"important":"enjoy","smell":[false,"difficult"]}')
blockchain.add_new_transaction(tx9)
blockchain.mine()

chain_id = blockchain.chain
print("-------------------------------------------")
print("Current blockchain from mining")
print(blockchain)
print("Is a valid chain? : " + str(blockchain.is_valid_chain(blockchain.chain)))
print("-------------------------------------------")
print("Saving chain to file...")
blockchain.chain_to_file("chain.txt")
print("File saved.")
print("-------------------------------------------")
tx10 = '{"forward":[-1907593984.0836291,false],"quietly":"certain"}'
print("Adding tx: " + tx10)
blockchain.add_new_transaction(tx10)
blockchain.mine()
print("Transaction added.")
print("-------------------------------------------")
print("Current blockchain from mining")
print(blockchain)
print("Is valid chain? : " + str(blockchain.is_valid_chain(blockchain.chain)))
print("-------------------------------------------")
print("Updating blockchain from file.")
blockchain.chain_from_file("chain.txt")
print("Updated.")
print("-------------------------------------------")
print("Current blockchain from mining. Last transaction should not appear.")
print(blockchain)
print("Is a valid chain? : " + str(blockchain.is_valid_chain(blockchain.chain)))
print("-------------------------------------------")

print("Previous chain: " + str(chain_id))
print("Current chain : " + str(blockchain.chain))

test_txt = " Hola012"
if test_txt.endswith('0' * 0):
    print("0*0")
else:
    print("Ni idea")
# print("Unconfirmed transactions (" + str(len(blockchain.unconfirmed_transactions)) + "): " + str(blockchain.unconfirmed_transactions))

#blockchain.chain[2].previous_hash = "holamariposa"
#check = blockchain.is_valid_chain(blockchain.chain)
#print(check)


#print(blockchain)
#print(blockchain.is_valid_chain(blockchain.chain))
#print(blockchain.chain[1].timestamp)
# print("Unconfirmed transactions (" + str(len(blockchain.unconfirmed_transactions)) + "): " + str(blockchain.unconfirmed_transactions))