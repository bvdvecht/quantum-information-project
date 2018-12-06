from random import randint
import time
import copy
from SimulaQron.cqc.pythonLib.cqc import CQCConnection, qubit

from gates import PrimitiveGate, CompositeGate, TensorGate, EntangleGate

class CustomGate(PrimitiveGate):
    def applyOn(self, qubits):
        qubits[0].rot_Z(64) # pi/4 rad

    def applyAdjointOn(self, qubits):
        qubits[0].rot_Z(64) # -pi/4 rad


# key and key_prev are Z_l and Z_{l-1} 
def send_D_Plus(alice, m, D, key, key_prev):
    alice.release_all_qubits()
    
    # create |+>^tensor(m)
    qubits = [qubit(alice) for i in range(m)]
    [ qb.H() for qb in qubits ]
    
    D.applyOn(qubits)
    
    # create encryption gates
    Z_prev = TensorGate(['Z' if bool(r) else 'I' for r in key_prev])
    Z = TensorGate(['Z' if bool(r) else 'I' for r in key])

    Z_prev.applyOn(qubits)
    Z.applyOn(qubits)

    
    for qb in qubits:
        print('alice send_D_Plus: send qbit')
        alice.sendQubit(qb, "Bob")
        print('alice send_D_Plus: qbit sent')

def createNextGate(m, D, measurements):
    # create tensor of X's (if meas=1) and I's (if meas=0)
    X = TensorGate(['X' if m else 'I' for m in measurements])
    D_dagger = copy.copy(D)
    D_dagger.adjoint = True

    # construct D_{l+1} = X_lD_lX_lD_dagger_l
    newD = CompositeGate([X, D, X, D_dagger])

    return newD


def main():
    with CQCConnection("Alice") as alice:  
        m = 2
        l = 3

        # HI = TensorGate(['H', 'I'])
        # CNOT = EntangleGate('CNOT')
        # G = CompositeGate([CNOT, HI])
        # G.applyOn(qubits)
        # print([qb.measure() for qb in qubits])

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

        # sum of measurement results from Bob
        cumul_meas = [ 0 for i in range(m) ]

        key = [ 0 for i in range(m) ]

        # protocol 1
        for i in range(l):
            key_prev = key
            # generate new random key
            key = [ randint(0, 1) for k in range(m) ]

            send_D_Plus(alice, m, D, key, key_prev)

            measurements = []
            for j in range(m):
                print("alice: receive measurement")
                meas = alice.recvClassical(close_after=True, timout=10)
                print('meas', int.from_bytes(meas, byteorder='big'))
                measurements.append(int.from_bytes(meas, byteorder='big'))
                print("alice: measurement received")

            # XOR measurements to cumul_meas for step
            cumul_meas = [(cumul_meas[k] + measurements[k])%2 for k in range(m)]

            # sleep since we don't use recvClassical atm which would block
            # time.sleep(5)

            D = createNextGate(m, D, measurements)

        
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