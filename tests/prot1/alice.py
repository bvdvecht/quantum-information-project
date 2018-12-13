from random import randint
import time
import copy
from SimulaQron.cqc.pythonLib.cqc import CQCConnection, qubit

from bqc.gates import PrimitiveGate, CompositeGate, TensorGate, EntangleGate
from bqc.prot1 import protocol1

def main():
    with CQCConnection("Alice") as alice:  
        m = 2
        l = 5

        # psi = |+>^tensor(m)
        psi = [ qubit(alice) for i in range(m) ]
        [ qb.H() for qb in psi ]

        # send psi to Bob
        for qb in psi:
            print('alice: send psi qubit')
            alice.sendQubit(qb, "Bob")
            print('alice: psi qubit sent')

        # gate to be applied to psi
        D = TensorGate(['Z', 'I'])
        print('initial gate D:', D)

        # sum of measurement results from Bob
        cumul_meas = protocol1(alice, m, l, D)
        
        result = []
        for i in range(m):
            result.append(alice.recvQubit())

        # result = XD|psi>, undo X:
        print('undoing X:', cumul_meas)
        for i in range(m):
            if cumul_meas[i] == 1:
                result[i].X()

        # measure result, should be |->|+>, i.e. 1 0 in H basis
        [qb.H() for qb in result]
        print("Result: ", result[0].measure(), result[1].measure())


main()