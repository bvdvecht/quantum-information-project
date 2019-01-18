from random import randint

from bqc.gates import CompositeGate, TensorGate
from bqc.gates import SimpleGate as SG
from bqc.prot2 import protocol2, send_D_Plus, protocol2_recv, recv_D_Plus
from bqc.byproducts import Byproduct, XRecord, ZRecord

CLASS_MSG_TIMEOUT_PROT3 = 100


def compute_target_gate_simple(j, p, N, M, X_record, Z_record, D):
    H = TensorGate([SG('H') for i in range(M)])
    # print('target gate H:', H)

    # X gate to undo byproduct of teleportation of previous iteration
    fixPrevXList = []
    for k in range(1, M + 1):
        gate = SG('X') if X_record.get(j - 1).get((p-1) * M + k) else SG('I')
        fixPrevXList.append(gate)
    fixPrevX = TensorGate(fixPrevXList)
    # print('target gate fixPrevX:', fixPrevX)

    # Z gate to undo byproduct of teleportation of previous iteration
    fixPrevZList = []
    for k in range(1, M + 1):
        gate = SG('Z') if Z_record.get(j - 1).get((p-1) * M + k) else SG('I')
        fixPrevZList.append(gate)
    fixPrevZ = TensorGate(fixPrevZList)
    # print('target gate fixPrevZ:', fixPrevZ)

    # Z gate to undo byproduct of teleportation of 2 iterations back
    fixPrevPrevZList = []
    for k in range(1, M + 1):
        gate = SG('Z') if Z_record.get(j - 2).get((p-1) * M + k) else SG('I')
        fixPrevPrevZList.append(gate)
    fixPrevPrevZ = TensorGate(fixPrevPrevZList)
    # print('target gate fixPrevPrevZ:', fixPrevPrevZ)


    targetD = CompositeGate(
        [H, fixPrevZ, H, D, fixPrevPrevZ, H, fixPrevX, fixPrevZ, H]
        )

    print('targetD:', targetD)
        
    return targetD


def compute_target_gate(j, p, N, M, X_record, Z_record, D):
    chi = {}
    zeta = {}

    if (j % 2) == 0:
        for k in range((p-1) * M + 1, p * M + 1):
            chi[k] = Z_record.get(j-1).get(k)

            zeta1 = Z_record.get(j-2).get(k)
            zeta2 = X_record.get(j-1).get(k)
            zeta3a = Z_record.get(j-3).get(k-1) + X_record.get(j-2).get(k-1)
            zeta3b = Z_record.get(j-3).get(k+1) + X_record.get(j-2).get(k+1)
            zeta[k] = (zeta1 + zeta2 + zeta3a + zeta3b) % 2

    else:
        for k in range((p-1) * M + 1, p * M + 1):
            chi1 = Z_record.get(j-1).get(k)
            chi2a = Z_record.get(j-2).get(k-1) + X_record.get(j-1).get(k-1)
            chi2b = Z_record.get(j-2).get(k+1) + X_record.get(j-1).get(k+1)
            chi[k] = (chi1 + chi2a + chi2b) % 2

            zeta[k] = (Z_record.get(j-2).get(k) + X_record.get(j-1).get(k)) % 2


    XjkGates = []
    for k in range((p-1) * M + 1, p * M + 1):
        XjkGates.append(SG('X') if chi[k] else SG('I'))

    ZjkGates = []
    for k in range((p-1) * M + 1, p * M + 1):
        ZjkGates.append(SG('Z') if zeta[k] else SG('I'))

    Xjk = TensorGate(XjkGates)
    Zjk = TensorGate(ZjkGates)

    targetD = CompositeGate([Xjk, D, Zjk, Xjk])
    return targetD


def protocol3(alice, J, N, L, D_gates, M, P, debug=False):
    X_record = XRecord(N)
    Z_record = ZRecord(N)

    # Send J to Bob
    alice.sendClassical("Bob", J, close_after=True)

    #-------#
    # j = 1 #
    #-------#

    # D_1
    D = D_gates[0]

    keyprev = [ 0 for i in range(N) ]
    key = [ randint(0, 1) for i in range(N) ]
    # key = [ 0 for i in range(N) ]
    
    Z_1 = Byproduct(N)
    for k in range(1, N+1):
        Z_1.set(k, key[k-1])

    Z_record.set(1, Z_1)

    # send_D_PLus(alice, N, D, Z_1, Z_0)
    send_D_Plus(alice, N, D, key, keyprev)


    #-------------#
    # j = 2,...,J #
    #-------------#

    for j in range(2, J + 1):
        print('ITERATION', j)

        xbyprod = Byproduct(N)
        X_record.set(j, xbyprod)
        
        zbyprod = Byproduct(N)
        Z_record.set(j, zbyprod)

        for p in range(1, P + 1):
            print('p =', p)
            targetD = compute_target_gate(j, p, N, M, X_record, Z_record, D_gates[j-1][p-1])
            if debug:
                print('alice iteration {} targetD:'.format(j))
                print(targetD)

            #Send flag to Bob when ready
            alice.sendClassical("Bob", 1, close_after=True)

            #Alice engages protocol 2 and saves the teleportation byproducts and her key
            Xj, Zj = protocol2(alice, M, L, targetD, no_encrypt=False, debug=False)
            print('alice iteration {} of prot3: prot2 returned:'.format(j))
            print('\tX:', Xj)
            print('\tZ:', Zj)
            assert len(Xj) == M and len(Zj) == M

            for k in range(1, M + 1):
                X_record.get(j).set((p-1) * M + k, Xj[k-1])

            for k in range(1, M + 1):
                Z_record.get(j).set((p-1) * M + k, Zj[k-1])

            


    #Receiving Bob's measurements in the X basis
    measurements = []
    for i in range(N):
        #print("alice: receive measurement")
        meas = alice.recvClassical(close_after=True, timout=CLASS_MSG_TIMEOUT_PROT3)
        print('alice: recveived final measurement:', int.from_bytes(meas, byteorder='big'))
        measurements.append(int.from_bytes(meas, byteorder='big'))
        #print("alice: measurement received")

    print('final Z:', Z_record.get(J))

    #Alice computes the output bits
    result = [ (measurements[k-1] + Z_record.get(J).get(k)) % 2 for k in range(1, N+1) ]

    return result


def protocol3_recv(bob, J, N, M, P, L, R):
    #Receives J=1 step qubits
    R = recv_D_Plus(bob, N)

    print('Bob end of iteration 1, contents of R:')
    R[0].Y()
    # R[1].Y()
    print('\n\n')
    
    for j in range(2, J + 1):
        print('\n\nBOB START ITERATION', j)

        if (j % 2) == 1:
            print('APPLYING CPHASE')
            [ R[i].cphase(R[i + 1]) for i in range(N - 1) ]
            print('Bob iteration {}, contents of R just after CZ:'.format(j))
            R[0].Y()
            # R[1].Y()
            print('\n\n')

        #Bob applies H
        print('APPLYING H')
        [ qb.H() for qb in R ]
        print('Bob iteration {}, contents of R just after H:'.format(j))
        R[0].Y()
        # R[1].Y()
        print('\n\n')

        for p in range(1, P + 1):
            #Wait for alice to be ready and avoid timeout
            flag = bob.recvClassical(close_after=True, timout=CLASS_MSG_TIMEOUT_PROT3)

            #Engage protocol 2
            R = protocol2_recv(bob, M, p, L, R)

        print("Bob depth", j, "done")
        print('Bob prot3 depth {} end, contents of R:'.format(j))
        R[0].Y()
        # R[1].Y()
        print('\n\n')


    #Bob measures in X basis
    for qb in R:
        qb.H()
        meas = qb.measure(inplace=True)
        qb.H()
        bob.sendClassical("Alice", meas, close_after=True)
