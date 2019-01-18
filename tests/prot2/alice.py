from SimulaQron.cqc.pythonLib.cqc import CQCConnection, qubit

from bqc.gates import TensorGate
from bqc.gates import SimpleGate as SG
from bqc.prot2 import protocol2_send


def main():
    with CQCConnection("Alice") as alice:  
        m = 2
        l = 1

        # psi = |+>^tensor(m)
        psi = [ qubit(alice) for i in range(m) ]
        [ qb.H() for qb in psi ]

        # send psi to Bob
        for qb in psi:
            #print('alice: send psi qubit')
            alice.sendQubit(qb, "Bob")
            #print('alice: psi qubit sent')

        # gate to be applied to psi
        D = TensorGate([SG('Z'), SG('I')])
        #D = EntangleGate('CPHASE')
        #rot = RotZGate(-ROT_PI_4)
        #D = TensorGate([rot, SG('I')])


        cumul_meas, key = protocol2_send(alice, m, l, D, debug=True, no_encrypt=False)

        
        result = []
        for i in range(m):
            result.append(alice.recvQubit())

        # result = ZXD|psi>

        # undo Z
        print('undoing Z:', key)
        for i in range(m):
            if key[i] == 1: # Z = Z_l = last key
                result[i].Z()

        # undo X
        print('undoing X:', cumul_meas)
        for i in range(m):
            if cumul_meas[i] == 1:
                result[i].X()

        # measure result, should be |->|+>, i.e. 1 0 in H basis
        [qb.H() for qb in result]
        print("Result: ", result[0].measure(), result[1].measure())


main()