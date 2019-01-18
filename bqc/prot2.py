from random import randint

from SimulaQron.cqc.pythonLib.cqc import qubit

from bqc.gates import CompositeGate, TensorGate
from bqc.gates import SimpleGate as SG

CLASS_MSG_TIMEOUT_PROT2 = 100

# key and key_prev are Z_l and Z_{l-1} 
def send_D_Plus(alice, m, D, key, key_prev):
    alice.release_all_qubits()
    
    # create |+>^tensor(m)
    qubits = [qubit(alice) for i in range(m)]
    [ qb.H() for qb in qubits ]
    
    D.applyTo(qubits)
    
    # create encryption gates
    Z_prev = TensorGate([SG('Z') if bool(r) else SG('I') for r in key_prev])
    Z = TensorGate([SG('Z') if bool(r) else SG('I') for r in key])

    Z_prev.applyTo(qubits)
    Z.applyTo(qubits)

    
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


def generate_key(m, no_encrypt):
    if no_encrypt:
        return [ 0 for i in range(m) ]
    else:
        return [ randint(0, 1) for i in range(m) ]


# set no_encrypt=True to have easier test case (all keys are 0)
def protocol2(alice, m, l, D, no_encrypt=False, debug=False):
    if debug:
        print('Alice: starting protocol 2')

    cumul_meas = [ 0 for i in range(m) ]
    key = [ 0 for i in range(m) ]

    # protocol 2
    for i in range(l):

        key_prev = key
        # generate new random key
        key = generate_key(m, no_encrypt)
        if debug:
            print('alice prot 2, sending gate D:', D)
        send_D_Plus(alice, m, D, key, key_prev)

        #logging.warning("     Alice waiting measurements")
        measurements = []
        for j in range(m):

            #print("alice: receive measurement")
            meas = alice.recvClassical(close_after=True, timout=CLASS_MSG_TIMEOUT_PROT2)

            #print('meas', int.from_bytes(meas, byteorder='big'))
            measurements.append(int.from_bytes(meas, byteorder='big'))
            #print("alice: measurement received")

        # XOR measurements to cumul_meas for step
        cumul_meas = [(cumul_meas[k] + measurements[k])%2 for k in range(m)]

        # sleep since we don't use recvClassical atm which would block
        # time.sleep(5)
        D = createNextGate(m, D, measurements)
        if debug:
            print("Alice prot2 iteration", i, "done")
            print('X byproducts:', measurements)
            print('key:', key)
            print('\n')

    return cumul_meas, key



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


def protocol2_recv(bob, m, p, l, R, debug=False):
    if debug:
        print('Bob: starting protocol 2')

    subR = R[(p-1) * m : p * m]

    for i in range(l):
        Rprime = recv_D_Plus(bob, m)
        measurements = teleport_proc(bob, m, subR, Rprime)
        for j in range(m):
            #print("bob: send measurement")
            bob.sendClassical("Alice", measurements[j], close_after=True)
            #print("bob: measurement sent")

        subR, Rprime = Rprime, subR

        if debug:
            print("Bob prot2 iteration", i, "done")
            print('Bob prot2 iteration {} end, contents of R:'.format(i))
            for qb in subR:
                qb.Y()
            print('\n')

    tempR = R[0 : (p-1) * m]
    tempR.extend(subR)
    tempR.extend(R[p * m :])
    R = tempR
    
    [qb.release for qb in Rprime]
    return R