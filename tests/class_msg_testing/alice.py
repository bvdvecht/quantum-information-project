from random import randint
import time
import copy
from SimulaQron.cqc.pythonLib.cqc import CQCConnection, qubit


def main():
    with CQCConnection("Alice") as alice:
        print('alice: waiting for msg')
        msg = alice.recvClassical(close_after=True, timout=10)
        print('alice: msg received', msg)

        print('alice: waiting for msg 2')
        msg = alice.recvClassical(close_after=True, timout=10)
        print('alice: msg 2 received', msg)


main()