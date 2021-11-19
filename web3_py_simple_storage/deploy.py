import json

from web3 import Web3

# # In the video, we forget to `install_solc`
# # from solcx import compile_standard
from solcx import compile_standard, install_solc

# import os
# from dotenv import load_dotenv

# load_dotenv()


with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()
    # print(simple_storage_file)

# # We add these two lines that we forgot from the video!
# print("Installing...")
install_solc("0.8.0")

# Solidity source code
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
    solc_version="0.8.0",
)
# print(compiled_sol)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# to deploy:
# 1. get bytecode: [] is the path in the .json file
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# 2. get abi
abi = json.loads(
    compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["metadata"]
)["output"]["abi"]

# w3 = Web3(Web3.HTTPProvider(os.getenv("RINKEBY_RPC_URL")))
# chain_id = 4

# For connecting to ganache: https://www.trufflesuite.com/ganache
# ganache is basically a javascript vm
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
chain_id = 1337
my_address = "0x2141394C8cb342A12039515b7198bF3E59afF178"
private_key = "0xe3b5ad3525b2274922dd8afc39cc2a2bf183f3768c891d0523fe509302257086"  # os.getenv("PRIVATE_KEY")

# 1. Create the contract in Python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
# print(SimpleStorage)

# Get the latest transaction, for POW.
nonce = w3.eth.getTransactionCount(my_address)
print("---- nonce: " + str(nonce))

# --- transaction
# 1. build a transaction, these 3 params are required.
transaction = SimpleStorage.constructor().buildTransaction(
    {"chainId": chain_id, "from": my_address, "nonce": nonce}
)
# print(transaction)

# 2. Sign the transaction with my private key
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
print("Deploying Contract!")

# 3. Send a transaction!
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
# Wait for the transaction to be mined, and get the transaction receipt
print("Waiting for transaction to finish...")

# 4. get a receipt for a transaction!
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(f"Done! Contract deployed to {tx_receipt.contractAddress}")


# Working with deployed Contracts
# to work with any smart contract, you need contract address and abi.
# google to get abi for existing contracts
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

# we can do call or transact (make a state change, it's not free).
# it's call(), it doesn't make state changes, so it's free.
print(f"Initial Stored Value {simple_storage.functions.retrieve().call()}")

print(f"Initial Stored Value {simple_storage.functions.store(15).call()}")
# returns 0, since we are not doing a transaction
print(f"Initial Stored Value {simple_storage.functions.retrieve().call()}")

# Making a transaction on the exiting contract
# this will update the states on the contract
# nonce can only be used once per transaction, so we do nonce + 1
greeting_transaction = simple_storage.functions.store(15).buildTransaction(
    {"chainId": chain_id, "from": my_address, "nonce": nonce + 1}
)
# sign it
signed_greeting_txn = w3.eth.account.sign_transaction(
    greeting_transaction, private_key=private_key
)

# send it
tx_greeting_hash = w3.eth.send_raw_transaction(signed_greeting_txn.rawTransaction)
print("Updating stored Value...")

# getting a receipt
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_greeting_hash)

# test it
print(simple_storage.functions.retrieve().call())
