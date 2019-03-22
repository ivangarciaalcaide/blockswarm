from bs_blockchain.Blockchain import Blockchain, Block


print("Testing...")

blockchain = Blockchain()
print(blockchain.chain[0].get_string_to_hash())
print(blockchain.chain[0].hash)
print("-----")
print(blockchain)
