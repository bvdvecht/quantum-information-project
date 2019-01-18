from SimulaQron.cqc.pythonLib.cqc import qubit

from bqc.gates import CompositeGate, TensorGate
from bqc.gates import SimpleGate as SG

CLASS_MSG_TIMEOUT_PROT1 = 100

def send_D_Plus(alice, m, D):
    # print('alice: releasing all qubits')
    # alice.release_all_qubits()

    #print('alice: creating new qubits')
    # create |+>^tensor(m)
    qubits = [qubit(alice) for i in range(m)]
    #print('alice:', len(qubits), 'qubits created')
    [ qb.H() for qb in qubits ]

    D.applyTo(qubits)

    for qb in qubits:
        #print('alice send_D_Plus: send qbit')
        alice.sendQubit(qb, "Bob")
        #print('alice send_D_Plus: qbit sent')


def createNextGate(m, D, measurements):
    # create tensor of X's (if meas=1) and I's (if meas=0)
    X = TensorGate([SG('X') if m else SG('I') for m in measurements])
    D_dagger = D.getDagger()

    # construct D_{l+1} = X_lD_lX_lD_dagger_l
    newD = CompositeGate([X, D, X, D_dagger])

    return newD


def protocol1(alice, m, l, D):
    print('Alice: starting protocol 1')

    cumul_meas = [ 0 for i in range(m) ]

    # protocol 1
    for i in range(l):
        print('alice: sending gate D_{} = {}'.format(i+1, str(D)))
        send_D_Plus(alice, m, D)

        measurements = []
        for j in range(m):
            #print("alice: receive measurement")
            meas = alice.recvClassical(close_after=True, timout=CLASS_MSG_TIMEOUT_PROT1)
            #print('meas', int.from_bytes(meas, byteorder='big'))
            measurements.append(int.from_bytes(meas, byteorder='big'))
            #print("alice: measurement received")

        # XOR measurements to cumul_meas for step
        cumul_meas = [(cumul_meas[i] + measurements[i])%2 for i in range(m)]

        D = createNextGate(m, D, measurements)
        print("Alice iteration", i, "done")
        print('X byproducts:', measurements)
        print('\n')

    return cumul_meas



def recv_D_Plus(bob, m):
    Rprime = []
    for i in range(m):
        #print("bob recv_D_Plus: receive qubit")
        Rprime.append(bob.recvQubit())
        #print("bob recv_D_Plus: qubit received")

    return Rprime

def teleport_proc(bob, m, R, Rprime):
    [ Rprime[i].cnot(R[i]) for i in range(m) ]
    return [ qb.measure(inplace=False) for qb in R ]


def protocol1_recv(bob, m, p, l, R):
    print('Bob: starting protocol 1')

    subR = R[p*m:(p+1)*m]

    for i in range(l):
        Rprime = recv_D_Plus(bob, m)
        measurements = teleport_proc(bob, m, subR, Rprime)
        for j in range(m):
            #print("bob: send measurement")
            bob.sendClassical("Alice", measurements[j], close_after=True)
            #print("bob: measurement sent")

        subR, Rprime = Rprime, subR

        print("Bob iteration", i, "done")
        print('contents of R:')
        for qb in subR:
            qb.Y()
        print('\n')

    tempR = R[0:p*m]
    tempR.extend(subR)
    tempR.extend(R[(p+1)*m:-1])
    R = tempR
    
    [qb.release for qb in Rprime]
    return R