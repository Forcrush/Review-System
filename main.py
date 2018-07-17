# -*- coding:utf-8 -*-
"""
Info:   This is a rudimentary frame of a anonymous system base on the idea of blockchain. You can run it to
        simulate the process of the real system. All parts are encapsulated well already, the command will 
        be illustraed when you run it, and the key word is 'chy'.

Author: 陈泓宇

Last modified time: 24th/May/2018
"""


import hashlib as hasher
import datetime as date
import random
import time


# ----------------------------------------------------------------
# about initializing


deposit = []  # record the deposit of contributor
reward = []  # record the reward of each reviewer
deposit_system = 1000  # record the total deposit of system


# initialize the reward list (reviewer's fortune list), default initialized number is 100
def initialize_reward():
    with open("reward_reviewer.txt", "w") as f:
        for _ in range(0, 100):
            f.write("0\n")


# initialize the reward list (reviewer's fortune list), default initialized number is 100
def initialize_deposit():
    with open("deposit_contributor.txt", "w") as f:
        for _ in range(0, 100):
            f.write("100\n")


# initialize the reward pool, default initialized number is 1000
def initialize_deposit_pool():
    with open("deposit_pool.txt", "w") as f:
        f.write("1000\n")


# load the reward info saved in txt
def load_reward_data():
    """
    with open("reward_reviewer.txt", "w") as f:
        for _ in range(0, 100):
            f.write("0\n")
    """
    for line in open("reward_reviewer.txt", "r"):
        reward.append(int(line))


# load the deposit info saved in txt
def load_deposit_data():
    """
    with open("reward_reviewer.txt", "w") as f:
        for _ in range(0, 100):
            f.write("0\n")
    """
    for line in open("deposit_contributor.txt", "r"):
        deposit.append(int(line))


# load the deposit pool info saved in txt
def load_deposit_pool():
    """
    with open("reward_reviewer.txt", "w") as f:
        for _ in range(0, 100):
            f.write("0\n")
    """
    global deposit_system
    for line in open("deposit_pool.txt", "r"):
        deposit_system = int(line)


# ---------------------------------------------------------------------
# About chainblock creation


class Block:
    review = 0  # check if reviewed: 0-not review | 1-pass | 2-no pass
    value = 3  # the review reward carried is 3 Bitcoin

    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.hash_block()

    def hash_block(self):
        sha = hasher.sha256()
        sha.update((str(self.index) +
                   str(self.timestamp) +
                   str(self.data) +
                   str(self.previous_hash)).encode("utf-8"))
        return sha.hexdigest()


def create_genesis_block():
    # Manually construct a block with
    # index zero and arbitrary previous hash
    s = "Genesis Block! This block is contributor " + str(paper[0].split(":")[0])
    return Block(0, date.datetime.now(), s, "0")


paper = []  # suppose for one paper-save pool we have 100 papers


def contributor_pool_to_paper():
    for p in range(0, len(contribute_pool)):
        # in paper list, each unit is "contributor's id : Article "
        paper.append(str(contribute_pool[p]) + ":" + "Article info")


def next_block(last_block):
    this_index = last_block.index + 1
    this_timestamp = date.datetime.now()
    # data: contributor's id + article
    this_data = "This block is contributor " + str(paper[this_index].split(":")[0])
    this_hash = last_block.hash
    return Block(this_index, this_timestamp, this_data, this_hash)


# create the genesis block
blockchain = []


# how many blocks should we add to the chain after the genesis block
# add blocks to the chain
def add_blocks_to_chain(num_of_blocks_to_add):
    previous_block = blockchain[0]
    for _ in range(0, num_of_blocks_to_add):
        block_to_add = next_block(previous_block)
        blockchain.append(block_to_add)
        previous_block = block_to_add
        # Tell everyone about it!


def print_chain():
    print("Block-Chain Info: ============================================")
    for i in range(0, len(blockchain)):
        print("Block #{} has been added to the blockchain!".format(blockchain[i].index))
        print("review: {}".format(blockchain[i].review))
        print("value: {}".format(blockchain[i].value))
        print("Data: {}".format(blockchain[i].data))
        print("timestamp: {}".format(blockchain[i].timestamp))
        print("Hash: {}\n".format(blockchain[i].hash))


# -----------------------------------------------------------------------------------
# about contributor


class Contributor:

    def __init__(self, id, dep):
        self.id = id
        self.dep = dep

    def contribute(self, num_paper):
        if self.dep < num_paper:
            print("contributor {} deposit not enough!".format(self.id))
            return
        self.dep -= num_paper * 3  # default cost is 3 per paper
        for _ in range(0, num_paper):
            contribute_pool.append(self.id)


# contributors list
contributor = []
# save the contributed paper's owner's id
contribute_pool = []


def create_contributor(number):
    for t in range(0, number):
        people = Contributor(t, deposit[t])
        contributor.append(people)


def contribution():
    print("begin contribution: ============================================\n")
    for p in range(0, len(contributor)):
        # simulate the contribution process, one contributor at most can contribute 5 papers
        contributor[p].contribute(random.randint(0, 5))


# -----------------------------------------------------------------------------------
# about distribution and review


class Reviewer:
    fortune = 0

    def __init__(self, id, paper_store):  # paper_store is a list(save the block)
        self.id = id
        self.paper_store = paper_store

    def review(self):
        global deposit_system
        if len(self.paper_store) == 0:
            return
        while self.paper_store:
            to_review = self.paper_store.pop()
            self.fortune += (to_review.value - 1)  # get a part of value of the paper
            deposit_system += 1  # put 1 to the deposit pool
            blockchain[to_review.index].value = 0
            # simulate the review process(set delay)
            time.sleep(random.uniform(0, 0.5))
            blockchain[to_review.index].review = random.randint(1, 2)


# reviewers list
reviewer = []
# in each pool units stores the papers to be reviewed by a certain reviewer
paper_pool = []


# create reviewers
def create_reviewer(number):
    for _ in range(0, number):
        paper_pool.append([])
    for t in range(0, number):
        people = Reviewer(t, paper_pool[t])
        # load the fortune data
        people.fortune = reward[t]
        reviewer.append(people)


# check if all the papers are reviewed
def review_finish():
    flag = True
    if len(blockchain) == 0:
        return flag
    for item in blockchain:
        if item.review == 0:
            flag = False
    return flag


# check if all the reviewers get the maximum number of papers
"""
def full_load():
    for item in paper_pool:
        if len(item) < 13:
            return False
    return True
"""


def distribution_review():
    # distribution
    print("begin distribution: ============================================\n")
    full_load = False  # check if full loaded which means each reviewers has its maximum number of papers to review
    while True:
        if review_finish():
            break
        if full_load:
            break
        for item in blockchain:
            if full_load:
                break
            if item.review == 0:
                who = random.randint(0, len(reviewer)-1)
                if len(paper_pool[who]) < 13:  # one contributor can at most choose 13 papers
                    paper_pool[who].append(item)
                    blockchain[item.index].review = 1  # temporary mark, representing this paper has been chosen
                else:
                    iteration_time = 0
                    while len(paper_pool[who]) >= 13:
                        if iteration_time == len(reviewer):
                            print("CAUTION : Need more reviewers ! There are surplus papers to be distributed !\n")
                            full_load = True
                            break
                        who = (who + 1) % len(reviewer)
                        iteration_time += 1
                    if not full_load:
                        paper_pool[who].append(item)
                        blockchain[item.index].review = 1  # temporary mark, represent this paper has been chosen
    # review
    print("begin review: ============================================\n")
    print("Some time needed ! Waiting...\n")
    for o in range(0, len(reviewer)):
        reviewer[o].paper_store = paper_pool[o]
    for p in reviewer:
        p.review()

    # record the fortune of reviewers
    with open("reward_reviewer.txt", "w") as f:
        for j in range(0, len(reward)):
            if j < len(reviewer):
                f.write("{}\n".format(reviewer[j].fortune))
            else:
                f.write("0\n")


# ---------------------------------------------------------------------
# about feedback -- if some contributor's paper have been passed, then he will get remuneration
def feedback():
    global deposit_system
    print("feedback process: ============================================\n")
    for b in blockchain:
        if b.review == 1:
            if deposit_system < 4:
                print("NO MONEY IN REWARD POOL !!!")  # check if there has enough money
                return
            deposit_system -= 4  # if pass, the money is given by deposit pool
            contributor[int(b.data.split(" ")[-1])].dep += 4  # if pass, contributor will get 2 Bitcoin per paper

    # record the deposit of contributors
    with open("deposit_contributor.txt", "w") as f:
        for j in range(0, len(deposit)):
            if j < len(contributor):
                f.write("{}\n".format(contributor[j].dep))
            else:
                f.write("0\n")

    # record the deposit of pool
    with open("deposit_pool.txt", "w") as f:
        f.write("{}\n".format(deposit_system))


def pre_main():

    load_reward_data()
    load_deposit_data()
    load_deposit_pool()

    """
    for t in range(0, 20):
        print(reward[t])
    """

    create_contributor(50)  # how many contributors you want to hire to review, can change the 50
    contribution()  # contributors begin to contribute

    """
    print(contribute_pool)
    for item in contributor:
        print(item.dep)
    """

    contributor_pool_to_paper()  # associate contributor_pool[] with paper[]

    blockchain.append(create_genesis_block())  # add genesis block in chain
    add_blocks_to_chain(len(paper)-1)  # how many blocks you want to add in the chain associated with papers in theory

    print_chain()

    create_reviewer(10)  # how many reviewers you want to hire to review, can change the 10
    distribution_review()

    print_chain()

    feedback()

    """
    for item in contributor:
        print(item.dep)
    """


# Extra part : string   <----Transformation---->   binary code
# string to binary code
def encode(string):
    encode_str = ' '.join([bin(ord(c)).replace('0b', '') for c in string])
    return encode_str


# binary code to string
def decode(string):
    decode_str = ''.join(chr(i) for i in [int(b, 2) for b in string.split(' ')])
    return decode_str


def main():
    print("\nExtirpating previous data and initializing them ----- Command 1")
    print("Running the program based on the previous data ----- Command 2\n")
    command = int(input("Command : "))

    while command != 2:
        if command == 1:
            initialize_reward()  # when you need to eradicate the previous info and rerun at the very beginning
            initialize_deposit()  # when you need to eradicate the previous info and rerun at the very beginning
            initialize_deposit_pool()  # when you need to eradicate the previous info and rerun at the very beginning
            print("\nData has been initialized successfully !")
            command = int(input("Command : "))
        else:
            print("\nWrong command ! Input again !\n")
            command = int(input("Command : "))

    keyword = ""
    print("\nInput the keyword to enjoy this program !\n")
    while keyword != decode("1100011 1101000 1111001"):
        keyword = input("Keyword : ")
        print("\nWrong keyword ! Input again !\n")
    print("======================\nMain program begin running...\n")
    pre_main()


main()
