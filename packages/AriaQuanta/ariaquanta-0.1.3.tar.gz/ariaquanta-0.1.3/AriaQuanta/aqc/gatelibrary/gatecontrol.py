
#import numpy as np

from AriaQuanta.aqc.gatelibrary import X, Z, P, S

from AriaQuanta._utils import np, swap_qubits, swap_qubits_density, is_unitary

#////////////////////////////////////////////////////////////////////////////////////
#------------------------------------------------------------------------------------
class GateControl:
    def __init__(self, name, base_gate_matrix, control_qubits, target_qubits):

        # control_qubits: List of qubits that control the gate (now only one qubit)
        # target_qubits: List of target qubits on which the gate will be applied if controls are satisfied
        # base_gate: The gate to apply on the target qubits (e.g., X, H, etc.)

        #name = f"C{'C' * (len(control_qubits) - 1)}{base_gate.name}"

        self.name = name
        base_gate_matrix = np.asarray(base_gate_matrix)
        self.base_gate_matrix = base_gate_matrix

        qubits = [control_qubits] + [target_qubits]
        qubits = np.asarray(qubits, dtype=int).flatten()

        control_qubits = [control_qubits]
        control_qubits = np.asarray(control_qubits, dtype=int).flatten()

        target_qubits = [target_qubits]
        target_qubits = np.asarray(target_qubits, dtype=int).flatten()

        self.control_qubits = control_qubits
        self.target_qubits = target_qubits
    
        self.qubits = qubits.tolist()

    def apply(self, num_of_qubits, multistate):

        base_gate_matrix = self.base_gate_matrix
        control_qubits = self.control_qubits
        target_qubits = self.target_qubits

        num_of_control_qubits = np.shape(control_qubits)[0]
        num_of_target_qubits = np.shape(target_qubits)[0]

        #-----------------------------------------------------
        # dim_of_controls = 2 * num_of_control_qubits # control_quibits is only 1 qubit at the moment (2 states)
        dim_of_targets = np.shape(base_gate_matrix)[0]
        dim = 2 * dim_of_targets
        control_matrix = np.identity(dim, dtype=complex) 

        for k1 in range(dim_of_targets, dim):
            for k2 in range(dim_of_targets, dim):
                control_matrix[k1, k2] = base_gate_matrix[k1 - dim_of_targets, k2 - dim_of_targets]
        #-----------------------------------------------------

        multistate_swaped = swap_qubits(0, control_qubits[0], num_of_qubits, multistate)

        for k1 in range(1, num_of_target_qubits+1):
            multistate_swaped = swap_qubits(k1, target_qubits[k1 - 1], num_of_qubits, multistate_swaped)

        if (num_of_qubits - num_of_control_qubits - num_of_target_qubits) > 0:
            dim = 2 ** (num_of_qubits - num_of_control_qubits - num_of_target_qubits)
            I2 = np.identity(dim, dtype=complex)
        else:
            I2 = 1  

        full_matrix = np.kron(control_matrix, I2)

        #if use_gpu_global:
        #    full_matrix = np.asnumpy(full_matrix)

        multistate_swaped = np.dot(full_matrix, multistate_swaped)

        for k1 in reversed(range(1, num_of_target_qubits+1)):
            multistate_swaped = swap_qubits(target_qubits[k1 - 1], k1, num_of_qubits, multistate_swaped)

        multistate = swap_qubits(control_qubits[0], 0, num_of_qubits, multistate_swaped)

        return multistate
    
    def apply_density(self, num_of_qubits, density_matrix):

        base_gate_matrix = self.base_gate_matrix
        control_qubits = self.control_qubits
        target_qubits = self.target_qubits

        num_of_control_qubits = np.shape(control_qubits)[0]
        num_of_target_qubits = np.shape(target_qubits)[0]

        #-----------------------------------------------------
        # dim_of_controls = 2 * num_of_control_qubits # control_quibits is only 1 qubit at the moment (2 states)
        dim_of_targets = np.shape(base_gate_matrix)[0]
        dim = 2 * dim_of_targets
        control_matrix = np.identity(dim, dtype=complex) 

        for k1 in range(dim_of_targets, dim):
            for k2 in range(dim_of_targets, dim):
                control_matrix[k1, k2] = base_gate_matrix[k1 - dim_of_targets, k2 - dim_of_targets]
        #-----------------------------------------------------

        density_matrix_swaped = swap_qubits_density(0, control_qubits[0], num_of_qubits, density_matrix)

        for k1 in range(1, num_of_target_qubits+1):
            density_matrix_swaped = swap_qubits_density(k1, target_qubits[k1 - 1], num_of_qubits, density_matrix_swaped)

        if (num_of_qubits - num_of_control_qubits - num_of_target_qubits) > 0:
            dim = 2 ** (num_of_qubits - num_of_control_qubits - num_of_target_qubits)
            I2 = np.identity(dim, dtype=complex)
        else:
            I2 = 1  

        full_matrix = np.kron(control_matrix, I2)

        #if use_gpu_global:
        #    full_matrix = np.asnumpy(full_matrix)

        density_matrix_swaped = full_matrix @ density_matrix_swaped @ np.conj(full_matrix.T)

        for k1 in reversed(range(1, num_of_target_qubits+1)):
            density_matrix_swaped = swap_qubits_density(target_qubits[k1 - 1], k1, num_of_qubits, density_matrix_swaped)

        density_matrix = swap_qubits_density(control_qubits[0], 0, num_of_qubits, density_matrix_swaped)

        return density_matrix    

#////////////////////////////////////////////////////////////////////////////////////
#///////// Control Gates /////////
#------------------------------------------------------------------------------------
class CX(GateControl):
    def __init__(self, control_qubits=0, target_qubits=1):  
        super().__init__(name='CX', base_gate_matrix=X().matrix, control_qubits=control_qubits, target_qubits=target_qubits) 

#------------------------------------------------------------------------------------
class CZ(GateControl):
    def __init__(self, control_qubits=0, target_qubits=1):  
        super().__init__(name='CZ', base_gate_matrix=Z().matrix, control_qubits=control_qubits, target_qubits=target_qubits)  

#------------------------------------------------------------------------------------
class CP(GateControl):
    def __init__(self, phi, control_qubits=0, target_qubits=1): 
        self.phi = phi 
        this_matrix = P(phi).matrix
        super().__init__(name='CP', base_gate_matrix=this_matrix, control_qubits=control_qubits, target_qubits=target_qubits)

#------------------------------------------------------------------------------------
class CS(GateControl):
    def __init__(self, control_qubits=0, target_qubits=1):  
        super().__init__(name='CS', base_gate_matrix=S().matrix, control_qubits=control_qubits, target_qubits=target_qubits)
#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
# 'Fred' in GateTripleQubit
#class CSWAP(GateControl):
#    def __init__(self, control_qubits=0, target_qubits=1): 
#        this_matrix = SWAP().matrix
#        super().__init__(name='CSWAP', base_gate_matrix=this_matrix, control_qubits=control_qubits, target_qubits=target_qubits)

#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
class CSX(GateControl):
    def __init__(self, control_qubits=0, target_qubits=1): 
        this_matrix = [[np.exp(+1j * np.pi / 4), np.exp(-1j * np.pi / 4)], 
                       [np.exp(-1j * np.pi / 4), np.exp(+1j * np.pi / 4)]] 
        super().__init__(name='CSX', base_gate_matrix=this_matrix, control_qubits=control_qubits, target_qubits=target_qubits) 

#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
# Control with an arbitray matrix - defined by the user
class CU(GateControl):
    def __init__(self, matrix, control_qubits=0, target_qubits=1):
        this_matrix = matrix
        CU.namedraw='CU'
        if is_unitary(this_matrix) == False:
            raise('Custom matrix is not unitary')
        super().__init__(name='CU', base_gate_matrix=this_matrix, control_qubits=control_qubits, target_qubits=target_qubits) 
                 
