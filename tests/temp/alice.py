from random import randint
import time
import copy
from SimulaQron.cqc.pythonLib.cqc import CQCConnection, qubit

from bqc.gates import PrimitiveGate, CompositeGate, TensorGate, EntangleGate


D1 = [0, 0]
D2 = [0, 0]
D3 = [0, 0]

Z1 = [1, 1]
Z2 = [1, 1]
Z3 = [0, 0]

X1 = [1, 1]
X2 = [1, 0]
X3 = [1, 1]

def main2():
    with CQCConnection("Alice") as alice:  
        R = [ qubit(alice) for i in range(2) ]
        
        # j = 1
        for i in range(2):
            R[i].H()

        # f(D1)
        for i in range(2):
            if D1[i]:
                R[i].Z()

        for i in range(2):
            if Z1[i]:
                R[i].Z()


        # j = 2
        for i in range(2):
            R[i].H()

        # f(D2)
        for i in range(2):
            R[i].H()
        for i in range(2):
            if Z1[i]:
                R[i].Z()
        for i in range(2):
            R[i].H()
        for i in range(2):
            if D2[i]:
                R[i].Z()
        for i in range(2):
            R[i].H()
        for i in range(2):
            if Z1[i]:
                R[i].Z()
        for i in range(2):
            R[i].H()

        # TP byproducts
        for i in range(2):
            if X2[i]:
                R[i].X()

        for i in range(2):
            if Z2[i]:
                R[i].Z()


        # j = 3
        for i in range(2):
            R[i].H()

        # f(D3)
        for i in range(2):
            R[i].H()
        for i in range(2):
            if Z2[i]:
                R[i].Z()
        for i in range(2):
            if X2[i]:
                R[i].X()
        for i in range(2):
            R[i].H()
        for i in range(2):
            if Z1[i]:
                R[i].Z()
        for i in range(2):
            if D3[i]:
                R[i].Z()
        for i in range(2):
            R[i].H()
        for i in range(2):
            if Z2[i]:
                R[i].Z()
        for i in range(2):
            R[i].H()

        # TP byproducts
        for i in range(2):
            if X3[i]:
                R[i].X()

        for i in range(2):
            if Z3[i]:
                R[i].Z()

        R[0].H()
        R[1].H()
        print('\n')
        print(R[0].measure())
        print(R[1].measure())
        return


def main():
    with CQCConnection("Alice") as alice:  
        R = [ qubit(alice) for i in range(2) ]
        
        # j = 1
        for i in range(2):
            R[i].H()

        # f(D1)
        for i in range(2):
            if D1[i]:
                R[i].Z()

        for i in range(2):
            if Z1[i]:
                R[i].Z()


        # j = 2
        for i in range(2):
            R[i].H()

        # f(D2)
        for i in range(2):
            if Z1[i]:
                R[i].X()

            if D2[i]:
                R[i].Z()

            if Z1[i]:
                R[i].X()

        # TP byproducts
        for i in range(2):
            if X2[i]:
                R[i].X()

        for i in range(2):
            if Z2[i]:
                R[i].Z()

        '''
        print('\n')
        print(R[0].measure())
        print(R[1].measure())
        return
        '''

        # j = 3
        R[0].cphase(R[1])

        for i in range(2):
            R[i].H()

        # f31(D3)
        if ((Z2[0] + Z1[1] + X2[1]) % 2) == 1:
            R[0].X()

        if ((Z1[0] + X2[0]) % 2) == 1:
            R[0].Z()

        if D3[0]:
            R[0].Z()

        if ((Z2[0] + Z1[1] + X2[1]) % 2) == 1:
            R[0].X()

        # f32(D3)
        if ((Z2[1] + Z1[0] + X2[0]) % 2) == 1:
            R[1].X()

        if ((Z1[1] + X2[1]) % 2) == 1:
            R[1].Z()

        if D3[1]:
            R[1].Z()

        if ((Z2[1] + Z1[0] + X2[0]) % 2) == 1:
            R[1].X()

        # TP byproducts
        for i in range(2):
            if X3[i]:
                R[i].X()

        for i in range(2):
            if Z3[i]:
                R[i].Z()

        # '''
        R[0].H()
        R[1].H()
        print('\n')
        print(R[0].measure())
        print(R[1].measure())
        # '''

        print('done')
main2()