class PrimitiveGate:
    def applyOn(self, qubit):
        pass

    def applyAdjoinOn(self, qubit):
        pass

# gate of length n that can be written as tensor product of n single-qubit gates
class TensorGate(PrimitiveGate):
    def __init__(self, gates):
        assert isinstance(gates, list), 'Gates should be provided in a list'
        for gate in gates:
            assert gate in ['X', 'Y', 'Z', 'H', 'I'], 'gate not supported: ' + gate
        self.dim = len(gates)
        self.gates = gates

    def applyOn(self, qubits):
        assert len(qubits) == self.dim
        for i in range(self.dim):
            if self.gates[i] == 'X':
                qubits[i].X()
            elif self.gates[i] == 'Y':
                qubits[i].Y()
            elif self.gates[i] == 'Z':
                qubits[i].Z()
            elif self.gates[i] == 'H':
                qubits[i].H()
            elif self.gates[i] == 'I':
                qubits[i].I()
            else:
                assert False, 'not implemented'

    def applyAdjointOn(self, qubits):
        self.applyOn(qubits) # for these gates, adjoint is the same

# gate than can not be written as a tensor product
# for now, only implements CNOT or CPHASE (2-qubit)
class EntangleGate(PrimitiveGate):
    def __init__(self, type):
        assert type in ['CNOT', 'CPHASE']
        self.type = type
        self.dim = 2

    def applyOn(self, qubits):
        assert len(qubits) == self.dim
        if self.type == 'CNOT':
            qubits[0].cnot(qubits[1])
        elif self.type == 'CPHASE':
            qubits[0].cphase(qubits[1])
        else:
            assert False, 'not implemented'



class CompositeGate:
    def __init__(self, gates, adjoint=False):
        assert isinstance(gates, list), 'CompositeGate constructor expects a list of gates'
        for gate in gates:
            assert isinstance(gate, PrimitiveGate) or isinstance(gate, CompositeGate)
        self.gates = gates
        self.adjoint = adjoint

    # if current gate is XYZ, first apply Z, then Y, etc.
    def applyOn(self, qubits):
        if self.adjoint:
            self.applyAdjointOn(qubits)
        else:
            for gate in reversed(self.gates):
                gate.applyOn(qubits)

    # if current gate is XYZ, to apply (XYZ)', do Z'Y'X' (' = dagger)
    def applyAdjointOn(self, qubits):
        for gate in self.gates:
            gate.applyAdjointOn(qubits)