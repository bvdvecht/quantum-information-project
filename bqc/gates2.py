import copy

class PrimitiveGate:
    def applyTo(self, qubit):
        pass

    def getDagger(self):
        return copy.deepcopy(self)


class SimpleGate(PrimitiveGate):
    def __init__(self, type):
        assert type in ['X', 'Y', 'Z', 'H', 'I'], 'gate not supported: ' + str(type)
        self.type = type

    def applyTo(self, qubit):
        if self.type == 'X':
            qubit.X()
        elif self.type == 'Y':
            qubit.Y()
        elif self.type == 'Z':
            qubit.Z()
        elif self.type == 'H':
            qubit.H()
        elif self.type == 'I':
            #qubit.I()
            pass
        else:
            assert False, 'not implemented'

    def getDagger(self):
        return copy.deepcopy(self)

    def __str__(self):
        return 'SimpleGate({})'.format(self.type)


# gate of length n that can be written as tensor product of n single-qubit gates
class TensorGate(PrimitiveGate):
    def __init__(self, gates):
        assert isinstance(gates, list), 'Gates should be provided in a list'
        #for gate in gates:
        #    assert gate in ['X', 'Y', 'Z', 'H', 'I'], 'gate not supported: ' + str(gate)
        self.dim = len(gates)
        self.gates = gates

    def applyTo(self, qubits):
        assert len(qubits) == self.dim
        for i in range(self.dim):

            if isinstance(self.gates[i], SimpleGate):
                self.gates[i].applyTo(qubits[i])

            elif isinstance(self.gates[i], EntangleGate):
                self.gates[i].applyTo([qubits[i], qubits[i+1]])

    def getDagger(self):
        cp = copy.deepcopy(self)
        daggerGates = []
        for gate in cp.gates:
            if gate is None:
                daggerGates.append(None)
            else:
                daggerGates.append(gate.getDagger())

        cp.gates = daggerGates
        return cp

    def __str__(self):
        s = 'tensor gate, gates:\n'
        for gate in self.gates:
            s += '\t' + str(gate) + '\n'
        return s


# gate than can not be written as a tensor product
# for now, only implements CNOT or CPHASE (2-qubit)
class EntangleGate(PrimitiveGate):
    def __init__(self, type):
        assert type in ['CNOT', 'CPHASE']
        self.type = type
        self.dim = 2

    def applyTo(self, qubits):
        assert len(qubits) == self.dim
        if self.type == 'CNOT':
            qubits[0].cnot(qubits[1])
        elif self.type == 'CPHASE':
            qubits[0].cphase(qubits[1])
        else:
            assert False, 'not implemented'
    
    def getDagger(self):
        return copy.deepcopy(self)

    def __str__(self):
        return 'entangle gate, ' + str(self.type)


class CompositeGate:
    def __init__(self, gates):
        assert isinstance(gates, list), 'CompositeGate constructor expects a list of gates'
        for gate in gates:
            assert isinstance(gate, PrimitiveGate) or isinstance(gate, CompositeGate)
        self.gates = gates

    # if current gate is XYZ, first apply Z, then Y, etc.
    def applyTo(self, qubits):
        for gate in self.gates:
            gate.applyTo(qubits)

    def getDagger(self):
        cp = copy.deepcopy(self)
        revDaggergates = []
        for gate in reversed(cp.gates):
            if gate is None:
                revDaggergates.append(None)
            else:
                revDaggergates.append(gate.getDagger())
        cp.gates = revDaggergates
        return cp

    def __str__(self):
        s = 'composite gate, gates:\n'
        for gate in self.gates:
            s += '\t' + str(gate) + '\n'
        return s


ROT_PI_2 = 64
ROT_PI_4 = 32

class RotZGate(PrimitiveGate):
    def __init__(self, angle):
        self.angle = angle % 256

    def applyTo(self, qubit):
        #print('applying rotZ to')
        #qubit.Y()
        qubit.rot_Z(self.angle)
        #print('result of rotZ:')
        #qubit.Y()

    def getDagger(self):
        cp = copy.deepcopy(self)
        cp.angle = (-cp.angle) % 256
        return cp

    def __str__(self):
        return 'RotZ({})'.format(self.angle)

