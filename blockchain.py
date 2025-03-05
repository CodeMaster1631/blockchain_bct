import time
from block import Block


class Blockchain:
    def __init__(self, difficulty: int = 4, reward: int = 50) -> list[Block]:
        self.chain: list[Block] = []
        self.difficulty = difficulty
        self.reward = reward
        self.balances = {}
        self.create_genesis_block()

    def create_genesis_block(self) -> None:
        genesis_block = Block(
            0, time.time(), "genesis block", "0", difficulty=self.difficulty
        )
        self.chain.append(genesis_block)

    def get_latest_block(self) -> Block:
        return self.chain[-1]

    def add_block(self, data: str) -> bool:
        prev_block = self.get_latest_block()
        # reward_transaction = f"{miner_address} was rewarded with {self.reward} coins"
        # data.append(reward_transaction)
        new_block = Block(
            len(self.chain),
            time.time(),
            data,
            prev_block.hash,
            difficulty=self.difficulty,
        )
        self.mine_block(new_block)
        self.chain.append(new_block)
        self.update_balances(data)
        return True

    def mine_block(self, block: Block) -> None:
        while not block.hash.startswith("0" * block.difficulty):
            block.nonce += 1
            block.hash = block.compute_hash()

    def display_blockchain(self) -> None:
        print("-" * 50)
        for block in self.chain:
            print(block)
            print("-" * 50)

    # def update_balances(self, transactions: list) -> None:
    #     for tx in transactions:
    #         if tx["from"] != "network":
    #             self.balances[tx["from"]] = (
    #                 self.balances.get(tx["from"], 0) - tx["amount"]
    #             )
    #         self.balances[tx["to"]] = self.balances.get(tx["to"], 0) + tx["amount"]

    def is_chain_valid(self) -> bool:
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            prev_block = self.chain[i - 1]

            if current_block.hash != current_block.compute_hash():
                print(f"Invalid hash at block {current_block.index}")
                return False

            if current_block.previous_hash != prev_block.hash:
                print(f"Invalid previous hash at block {current_block.index}")
                return False

        return True
