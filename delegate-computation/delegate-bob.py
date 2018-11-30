from SimulaQron.cqc.pythonLib.cqc import CQCConnection, qubit

def main():
    with CQCConnection("Bob") as bob:
        psi = bob.recvQubit()
        psi.X()
        bob.sendQubit(psi, "Alice")

main()