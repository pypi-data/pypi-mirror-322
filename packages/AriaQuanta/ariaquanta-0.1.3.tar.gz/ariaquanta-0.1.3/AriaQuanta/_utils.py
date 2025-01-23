#import numpy as np

from AriaQuanta.config import Config, get_array_module

#------------------------------------------------------------------------------------
np = get_array_module(Config.use_gpu)

#------------------------------------------------------------------------------------
def is_unitary(matrix):
    return np.allclose(matrix @ matrix.conj().T, np.eye(matrix.shape[0]), atol=1e-10)

#------------------------------------------------------------------------------------
def swap_qubits(idx1, idx2, num_of_qubits, multistate):

    indices_swaped = []
    size = 2 ** num_of_qubits
    
    #---------------------------------
    for i in range(size):

        state_str = format(i, '0{}b'.format(num_of_qubits))
        #print('-----------')
        #print(state_str)

        new_state_str = state_str[:idx1] + state_str[idx2] + state_str[idx1+1:]
        new_state_str = new_state_str[:idx2] + state_str[idx1] + new_state_str[idx2+1:]

        #print(new_state_str)
        
        index_swaped = int(new_state_str, 2)

        #print(index_original, index_swaped)
        indices_swaped.append(index_swaped)

    multistate_swaped = multistate[indices_swaped]
    return multistate_swaped

#------------------------------------------------------------------------------------
def swap_qubits_density(idx1, idx2, num_of_qubits, density_matrix):

    indices_swaped = []
    size = 2 ** num_of_qubits
    
    #---------------------------------
    for i in range(size):

        state_str = format(i, '0{}b'.format(num_of_qubits))
        #print('-----------')
        #print(state_str)

        new_state_str = state_str[:idx1] + state_str[idx2] + state_str[idx1+1:]
        new_state_str = new_state_str[:idx2] + state_str[idx1] + new_state_str[idx2+1:]

        #print(new_state_str)
        
        index_swaped = int(new_state_str, 2)

        #print(index_original, index_swaped)
        indices_swaped.append(index_swaped)

    density_matrix_swaped = density_matrix
    density_matrix_swaped = density_matrix_swaped[:,indices_swaped]
    density_matrix_swaped = density_matrix_swaped[indices_swaped,:]

    return density_matrix_swaped