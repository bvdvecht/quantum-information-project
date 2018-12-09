from random import randint
import time
import copy
from SimulaQron.cqc.pythonLib.cqc import CQCConnection, qubit

from gates import PrimitiveGate, CompositeGate, TensorGate, EntangleGate

def prepare_D_Plus(alice, m, D):
    print('alice: creating new qubits')
    # create |+>^tensor(m)
    qubits = [qubit(alice) for i in range(m)]
    print('alice:', len(qubits), 'qubits created')
    [ qb.H() for qb in qubits ]

    D.applyOn(qubits)
    return qubits


def createNextGate(m, D, measurements):
    # create tensor of X's (if meas=1) and I's (if meas=0)
    X = TensorGate(['X' if meas else 'I' for meas in measurements])
    D_dagger = copy.copy(D)
    print('alice: D_dagger:', D_dagger)
    D_dagger.adjoint = True

    # construct D_{l+1} = X_lD_lX_lD_dagger_l
    newD = CompositeGate([X, D, X, D_dagger])
    print('alice: newD:', newD)

    return newD


def main():
    with CQCConnection("Alice") as alice:  
        m = 2
        l = 2

        # psi = |+>^tensor(m)
        psi = [ qubit(alice) for i in range(m) ]
        [ qb.H() for qb in psi ]

        # gate to be applied to psi
        D = TensorGate(['Z', 'Z'])
        print('initial gate D:', D)

        cumul_meas = [ 0 for i in range(m) ]

        for i in range(l):
            # prepare D_Plus
            dplus = prepare_D_Plus(alice, m, D)
            print('psi:', psi)
            print('dplus:', dplus)

            [ dplus[i].cnot(psi[i]) for i in range(m) ]
            # inplace=False !!
            meas = [ qb.measure(inplace=False) for qb in psi ]

            psi = dplus

            cumul_meas = [(cumul_meas[i] + meas[i])%2 for i in range(m)]
            
            D = createNextGate(m, D, meas)

        result = psi

        print('undoing X:', cumul_meas)
        for i in range(m):
            if cumul_meas[i] == 1:
                result[i].X()

        # measure result, should be |->|+>, i.e. 1 0 in H basis
        [qb.H() for qb in result]
        print("Result: ", result[0].measure(), result[1].measure())

main()