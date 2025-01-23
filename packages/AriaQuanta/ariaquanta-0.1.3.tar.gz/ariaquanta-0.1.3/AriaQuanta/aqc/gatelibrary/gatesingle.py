
#import numpy as np
from AriaQuanta._utils import np, swap_qubits, is_unitary

#////////////////////////////////////////////////////////////////////////////////////

class GateSingleQubit:
    def __init__(self, name, matrix, target_qubit):
        
        self.name = name
        matrix = np.asarray(matrix)
        self.matrix = matrix

        target_qubit = [target_qubit]
        target_qubit = np.asarray(target_qubit, dtype=int).flatten()
        self.target_qubit = target_qubit

        self.qubits = target_qubit.tolist()
        
    #----------------------------------------------
    def apply(self, num_of_qubits, multistate):
        
        target_qubit = self.target_qubit

        if target_qubit[0] > 0:
            dim = 2 ** target_qubit[0]
            I1 = np.identity(dim, dtype=complex)
        else:
            I1 = 1
        if (num_of_qubits - target_qubit[0] - 1) > 0:
            dim = 2 ** (num_of_qubits - target_qubit[0] - 1)
            I2 = np.identity(dim, dtype=complex)
        else:
            I2 = 1         
    
        full_matrix = np.kron(I1, self.matrix)
        full_matrix = np.kron(full_matrix, I2)
        
        multistate = np.dot(full_matrix, multistate)

        return multistate
    
    #----------------------------------------------
    def apply_density(self, num_of_qubits, density_matrix):
        
        target_qubit = self.target_qubit

        if target_qubit[0] > 0:
            dim = 2 ** target_qubit[0]
            I1 = np.identity(dim, dtype=complex)
        else:
            I1 = 1
        if (num_of_qubits - target_qubit[0] - 1) > 0:
            dim = 2 ** (num_of_qubits - target_qubit[0] - 1)
            I2 = np.identity(dim, dtype=complex)
        else:
            I2 = 1         
    
        full_matrix = np.kron(I1, self.matrix)
        full_matrix = np.kron(full_matrix, I2)
        
        density_matrix = full_matrix @ density_matrix @ np.conj(full_matrix.T)

        return density_matrix

#////////////////////////////////////////////////////////////////////////////////////
#///////// 1-Qubit Gates /////////
#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
class I(GateSingleQubit):
    def __init__(self, target_qubit=0):
        matrix = np.eye(2)
        super().__init__(name='I', matrix=matrix, target_qubit=target_qubit)

#------------------------------------------------------------------------------------
class Ph(GateSingleQubit):
    def __init__(self, delta, target_qubit=0):
        self.delta = delta
        matrix = np.exp(+1j * delta) * np.eye(2)
        super().__init__(name='Ph', matrix=matrix, target_qubit=target_qubit)

#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
class X(GateSingleQubit):
    def __init__(self, target_qubit=0):
        matrix = np.array([[0, 1], [1, 0]])
        super().__init__(name='X', matrix=matrix, target_qubit=target_qubit)

#------------------------------------------------------------------------------------
class Y(GateSingleQubit):
    def __init__(self, target_qubit=0):
        matrix = np.array([[0, -1j], [1j, 0]])
        super().__init__(name='Y', matrix=matrix, target_qubit=target_qubit)

#------------------------------------------------------------------------------------
class Z(GateSingleQubit):
    def __init__(self, target_qubit=0):
        matrix = np.array([[1, 0], [0, -1]])
        super().__init__(name='Z', matrix=matrix, target_qubit=target_qubit)

#------------------------------------------------------------------------------------
class S(GateSingleQubit):
    def __init__(self, target_qubit=0):
        matrix = np.array([[1, 0], [0, 1j]])
        super().__init__(name='S', matrix=matrix, target_qubit=target_qubit)

#------------------------------------------------------------------------------------
class Xsqrt(GateSingleQubit):
    def __init__(self, target_qubit=0):
        matrix = 1/2 * np.array([[1+1j, 1-1j], [1-1j, 1+1j]])
        super().__init__(name='Xsqrt', matrix=matrix, target_qubit=target_qubit)

#------------------------------------------------------------------------------------
class H(GateSingleQubit):
    def __init__(self, target_qubit=0):
        matrix = (1 / np.sqrt(2)) * np.array([[1, 1], [1, -1]])
        super().__init__(name='H', matrix=matrix, target_qubit=target_qubit)  

#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
class P(GateSingleQubit):
    def __init__(self, phi, target_qubit=0):
        self.phi = phi
        matrix = np.array([[1, 0], [0, np.exp(1j * phi)]])
        super().__init__(name='P', matrix=matrix, target_qubit=target_qubit)

#------------------------------------------------------------------------------------
class T(GateSingleQubit):
    def __init__(self, target_qubit=0):
        matrix = np.array([[1, 0], [0, np.exp(1j * np.pi / 4)]])
        super().__init__(name='T', matrix=matrix, target_qubit=target_qubit)

#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
class RX(GateSingleQubit):
    def __init__(self, theta, target_qubit=0):
        self.theta = theta
        matrix = np.array([
            [np.cos(self.theta / 2), -1j * np.sin(self.theta / 2)],
            [-1j * np.sin(self.theta / 2), np.cos(self.theta / 2)]
        ])
        super().__init__(name='RX', matrix=matrix, target_qubit=target_qubit)

#------------------------------------------------------------------------------------
class RY(GateSingleQubit):
    def __init__(self, theta, target_qubit=0):
        self.theta = theta
        matrix = np.array([
            [np.cos(self.theta / 2), -np.sin(self.theta / 2)],
            [np.sin(self.theta / 2), np.cos(self.theta / 2)]
        ])
        super().__init__(name='RY', matrix=matrix, target_qubit=target_qubit)

#------------------------------------------------------------------------------------
class RZ(GateSingleQubit):
    def __init__(self, theta, target_qubit=0):
        self.theta = theta
        matrix = np.array([
            [np.exp(-1j * self.theta / 2), 0.0],
            [0.0, np.exp(1j * self.theta / 2)]
        ])
        super().__init__(name='RZ', matrix=matrix, target_qubit=target_qubit)  

#------------------------------------------------------------------------------------ 
class Rot(GateSingleQubit):
    def __init__(self, theta, phi, lambda_, target_qubit=0):
        self.theta = theta
        self.phi = phi
        self.lambda_ = lambda_
        matrix = np.array([
            [np.cos(self.theta / 2), -np.exp(1j * self.lambda_) * np.sin(self.theta / 2)],
            [np.exp(1j * self.phi) * np.sin(self.theta / 2), np.exp(1j * (self.lambda_ + self.phi)) * np.cos(self.theta / 2)]
        ])
        super().__init__(name='Rot', matrix=matrix, target_qubit=target_qubit)   







    
     
   
