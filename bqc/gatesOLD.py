class PrimitiveGate:
    def applyOn(self, qubit):
        pass

    def applyAdjointOn(self, qubit):
        pass

# gate of length n that can be written as tensor product of n single-qubit gates
class TensorGate(PrimitiveGate):
    def __init__(self, gates, adjoint=False):
        assert isinstance(gates, list), 'Gates should be provided in a list'
        #for gate in gates:
        #    assert gate in ['X', 'Y', 'Z', 'H', 'I'], 'gate not supported: ' + str(gate)
        self.dim = len(gates)
        self.gates = gates
        self.adjoint = adjoint

    def applyOn(self, qubits):
        assert len(qubits) == self.dim
        if self.adjoint:
            self.applyAdjointOn(qubits)
        else:
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
                    #assert False, 'not implemented'
                    self.gates[i].applyOn([qubits[i]])

    def applyAdjointOn(self, qubits):
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
                #assert False, 'not implemented'
                self.gates[i].applyAdjointOn([qubits[i]])

    def __str__(self):
        gate_list = [ str(gate) if isinstance(gate, RotZGate) else gate for gate in self.gates ]
        return 'tensor gate, gates:' + str(gate_list)

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

    
    def applyAdjointOn(self, qubits):
        self.applyOn(qubits) # for these gates, adjoint is the same

    def __str__(self):
        return 'entangle gate, ' + str(self.type)



class CompositeGate:
    def __init__(self, gates, adjoint=False):
        assert isinstance(gates, list), 'CompositeGate constructor expects a list of gates'
        for gate in gates:
            assert isinstance(gate, PrimitiveGate) or isinstance(gate, CompositeGate) or isinstance(gate, EntangleGate)
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


    def __str__(self):
        s = 'composite gate, gates:\n'
        for gate in self.gates:
            s += '\t' + str(gate) + '\n'

        return s


ROT_PI_2 = 64
ROT_PI_4 = 32

class RotZGate(PrimitiveGate):
    def __init__(self, angle, adjoint=False):
        self.angle = angle % 256
        self.adjoint = adjoint

    def applyOn(self, qubits):
        if self.adjoint:
            self.applyAdjointOn(qubits)
        else:
            assert(len(qubits) == 1)
            #print('applying rotZ on')
            #qubits[0].Y()
            qubits[0].rot_Z(self.angle)
            #print('result of rotZ:')
            #qubits[0].Y()

    def applyAdjointOn(self, qubits):
        assert(len(qubits) == 1)
        qubits[0].rot_Z((-self.angle)%256)

    def __str__(self):
        angle = self.angle
        if self.adjoint:
            angle = (- angle) % 256
        return 'RotZ({})'.format(angle)


class CustomDiagonalGate(PrimitiveGate):

    # Gate of type exp(i(2*pi*n_0/256*I + 2*pi*n_1/256*Z))

    # In this case, we can forget about the I gate since it will count only as a global phase on the system

    # !!! WORKS ONLY FOR SINGLE-QUBIT

    def __init__(self, steps, adjoint=False):

        #steps[0] is phase of identity in the form steps*2*pi/256 radians
        #steps[1] is phase of Z

        assert isinstance(steps, list), 'CompositeGate constructor expects a list of diagonal '
        assert(len(steps)==2), 'Expected two elements for the rotation steps'

        for i in range(len(steps)):
            steps[i] = (-2*steps[i])%256
            # print('steps[{}] = {}'.format(i, str(steps[i])))

        self.steps = steps
        self.adjoint = adjoint

    def applyOn(self, qubits):
        if self.adjoint:
            self.applyAdjointOn(qubits)
        else:
            assert(len(qubits)==1)
            qubits[0].rot_Z(self.steps[1])


    def applyAdjointOn(self, qubits):
        assert(len(qubits)==1)
        qubits[0].rot_Z((-self.steps[1])%256)


    def __str__(self):
        s = '1-qubit DGate:\n'
        return s
