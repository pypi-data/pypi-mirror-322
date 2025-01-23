
#import numpy as np
from AriaQuanta._utils import np

class Qubit:
    def __init__(self, state=np.array([[1], [0]])):
        self.state = state
        
class MultiQubit:
    def __init__(self, num_of_qubits):  # num_of_qubit, multistate, qubits

        qubits = [] 
 
        qubit_0 = Qubit()
        qubits.append(qubit_0)
        multistate = qubit_0.state

        for i in range(1, num_of_qubits):
            qubit_i = Qubit()
            state_i = qubit_i.state

            qubits.append(qubit_i)
            multistate = np.kron(multistate, state_i)

        MultiQubit.num_of_qubits = num_of_qubits    
        MultiQubit.multistate = multistate
        MultiQubit.qubits = qubits

        