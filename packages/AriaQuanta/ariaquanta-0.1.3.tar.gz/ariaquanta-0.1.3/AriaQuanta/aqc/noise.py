
#import numpy as np
from AriaQuanta._utils import np, swap_qubits, is_unitary
from AriaQuanta.aqc.gatelibrary import X, Y, Z

"""
Currently, 
- I am applying bit-type noises (applied to statevector)
- Only once and at the end of the run of a circuit (in the backend/job.py),
- I apply noise by probability p, to a randomly chosen qubit 
- [Another option could be appling just after the gate and on the target_qubit itself]
"""
#////////////////////////////////////////////////////////////////////////////////////

class NoiseClass:

    def __init__(self, name, noise_gate, probability, target_qubit):
        
        self.name = name
        self.noise_gate = noise_gate    
        self.probability = probability
        self.target_qubit = target_qubit

    def apply(self, num_of_qubits, multistate):

        p = np.random.rand(1)[0]
        if p < self.probability:
            if self.target_qubit == -1:
                q = np.random.randint(0, high=num_of_qubits, size=1, dtype=int)
            else:
                q = self.target_qubit

            this_gate = self.noise_gate
            multistate = this_gate(q).apply(num_of_qubits, multistate)

        return multistate
    
    def apply_noise_density(self, num_of_qubits, density_matrix):
        return 1

#------------------------------------------------------------------------------------
class BitFlipNoise(NoiseClass):
    def __init__(self, probability=1.0, target_qubit=-1):
        noise_gate = X
        super().__init__(name='BitFlip', noise_gate=noise_gate, probability=probability, target_qubit=target_qubit)
    
#------------------------------------------------------------------------------------
class PhaseFlipNoise(NoiseClass):
    def __init__(self, probability=1.0, target_qubit=-1):
        noise_gate = Z
        super().__init__(name='PhaseFlip', noise_gate=noise_gate, probability=probability, target_qubit=target_qubit)

#------------------------------------------------------------------------------------
class DepolarizingNoise(NoiseClass):
    def __init__(self, probability=1.0, target_qubit=-1):
        #choose_gate = np.random.choice(['XGate','YGate','ZGate'])

        noise_gate = Y

        #if choose_gate == 'XGate':
        #    noise_gate = X
        #elif choose_gate == 'YGate':
        #    noise_gate = Y
        #elif choose_gate == 'ZGate':
        #    noise_gate = Z

        super().__init__(name='Depolarizing', noise_gate=noise_gate, probability=probability, target_qubit=target_qubit)
    

#------------------------------------------------------------------------------------
# BitFlip:
#def apply_noise(self, num_of_qubits, multistate_or_densitymatrix):
#    """Apply bit flip noise to a quantum state."""
#    size = 2 ** num_of_qubits
#    bit_flip_matrix = np.eye(size, dtype=complex) * (1 - self.probability)
#    for i in range(size):
#        flip_index = i ^ 1  # Flip the least significant bit
#        bit_flip_matrix[i, flip_index] = self.probability
#    return np.dot(bit_flip_matrix, multistate_or_densitymatrix)    

#------------------------------------------------------------------------------------
# DepolarizingNoise:
#def apply_noise(self, num_of_qubits, multistate_or_densitymatrix):
#    """Apply depolarizing noise to a quantum state."""
#    size = 2 ** num_of_qubits
#    depolarizing_matrix = np.eye(size, dtype=complex) * (1 - self.probability) + \
#                          (self.probability / size) * np.ones((size, size), dtype=complex)
#    return np.dot(depolarizing_matrix, multistate_or_densitymatrix)