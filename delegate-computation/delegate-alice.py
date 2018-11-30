from SimulaQron.cqc.pythonLib.cqc import CQCConnection, qubit

def main():
    with CQCConnection("Alice") as alice:
        psi = qubit(alice) # prepare |0> state
        alice.sendQubit(psi, "Bob")

        Xpsi = alice.recvQubit() # receive X|0> computed by Bob
        print(Xpsi.measure())

main()