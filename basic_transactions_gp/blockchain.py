import hashlib
import json
from time import time
from uuid import uuid4

from flask import Flask, jsonify, request


class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.new_block(previous_hash=1, proof=100)

    def new_transaction(self, sender, recipient, amount):
        self.current_transactions.append({
            "sender": sender,
            "recipient": recipient,
            "amount": amount
        })
        return len(self.chain)

    def new_block(self, proof, previous_hash=None):
        """
        Create a new Block in the Blockchain

        A block should have:
        * Index
        * Timestamp
        * List of current transactions
        * The proof used to mine this block
        * The hash of the previous block

        :param proof: <int> The proof given by the Proof of Work algorithm
        :param previous_hash: (Optional) <str> Hash of previous Block
        :return: <dict> New Block
        """

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.last_block)
        }
        self.current_transactions = []
        self.chain.append(block)
        return block

    def hash(self, block):
        """
        Creates a SHA-256 hash of a Block

        :param block": <dict> Block
        "return": <str>
        """
        string_block = json.dumps(block, sort_keys=True)
        raw_hash = hashlib.sha256(string_block.encode())
        hex_hash = raw_hash.hexdigest()
        return hex_hash

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def valid_proof(block_string, proof):
        """
        Validates the Proof:  Does hash(block_string, proof) contain 3
        leading zeroes?  Return true if the proof is valid
        :param block_string: <string> The stringified block to use to
        check in combination with `proof`
        :param proof: <int?> The value that when combined with the
        stringified previous block results in a hash that has the
        correct number of leading zeroes.
        :return: True if the resulting hash is a valid proof, False otherwise
        """
        guess = f'{block_string}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:6] == "000000"


app = Flask(__name__)
node_identifier = str(uuid4()).replace('-', '')
blockchain = Blockchain()


@app.route('/transactions/new', methods=['POST'])
def transaction():
    data = request.get_json()
    if 'sender' not in data or 'recipient' not in data or 'amount' not in data:
        return jsonify({
            'message': 'Missing sender/recipient/amount'
        }), 400
    block_id = blockchain.new_transaction(
        data['sender'], data['recipient'], data['amount'])
    return jsonify({
        'message': block_id
    }), 200


@app.route('/mine', methods=['POST'])
def mine():
    data = request.get_json()
    if 'proof' not in data or 'id' not in data:
        return jsonify({
            'message': 'Missing proof/id'
        }), 400
    proof = data['proof']
    block_string = json.dumps(blockchain.last_block, sort_keys=True)
    if not blockchain.valid_proof(block_string, proof):
        return jsonify({
            'message': f'Invalid proof'
        }), 400
    previous_hash = blockchain.hash(blockchain.last_block)
    block = blockchain.new_block(proof, previous_hash)
    blockchain.new_transaction(0, id, 1)
    response = {
        'new_block': block,
        'message': 'New Block Forged'
    }
    return jsonify(response), 200


@app.route('/last_block', methods=['GET'])
def last_block():
    return jsonify(blockchain.last_block), 200


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    return jsonify(response), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
