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


def send_D_Plus(alice, m, D):
    alice.release_all_qubits()
    qubits = [qubit(alice) for i in range(m)]
    [ qb.H() for qb in qubits ]
    D.applyOn(qubits)
    print('sending qubits to Bob')
    for qb in qubits:
        alice.sendQubit(qb, "Bob")
    print('qubit sent to Bob')

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
        l = 2

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
            alice.sendQubit(qb, "Bob")

        # gate to be applied to psi
        D = TensorGate(['Z', 'I'])

        # sum of measurement results from Bob
        cumul_meas = [0 for i in range(m)]

        # protocol 1
        for i in range(l):
            send_D_Plus(alice, m, D)

            # for now, since classical messages seem a bit buggy
            measurements = [ bool(randint(0, 1)) for i in range(m) ]
            # for i in range(m):
            #    measurements.append(alice.recvClassical(close_after=False))

            # XOR measurements to cumul_meas for step
            cumul_meas = [(cumul_meas[i] + measurements[i])%2 for i in range(m)]

            # sleep since we don't use recvClassical atm which would block
            time.sleep(5)

            D = createNextGate(m, D, measurements)

        
        result = []
        for i in range(m):
            result.append(alice.recvQubit())

        # result = XD|psi>, undo X:
        for i in range(m):
            if cumul_meas[i] == 1:
                result[i].X()

        # measure result, should be |->, i.e. 1 in H basis
        [qb.H() for qb in result]
        print("Result: ", result[0].measure(), result[1].measure())


main()