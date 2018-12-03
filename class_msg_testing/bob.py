from SimulaQron.cqc.pythonLib.cqc import CQCConnection, qubit

def main():
    with CQCConnection("Bob") as bob:
        print("bob: sending msg")
        bob.sendClassical("Alice", 12, close_after=True)
        print("bob: msg sent")

        print("bob: sending msg 2")
        bob.sendClassical("Alice", 67, close_after=True)
        print("bob: msg 2 sent")
        
        


main()