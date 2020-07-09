from art import *
import random
from players_braket.oracle_prophecies import *


def roll_to_ascii(roll_list):
    for roll in roll_list:
            if roll != 20:
                tprint(str(roll))
            else:
                tprint(str(roll), font="rnd-large")


def stalling_message():
    fortune = bool(random.getrandbits(1))

    if fortune:
        fname = 'oracle_prophecies/python_fortunes'
    if not fortune:
        fname = 'oracle_prophecies/python_literature'

    raw_lines = open(fname).read().split('%')

    print(random.choice(raw_lines))


if __name__=='__main__':
    stalling_message()

