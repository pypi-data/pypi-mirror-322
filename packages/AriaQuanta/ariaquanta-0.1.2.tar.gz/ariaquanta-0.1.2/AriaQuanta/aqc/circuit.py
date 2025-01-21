
#import numpy as np
import matplotlib.pyplot as plt
from copy import deepcopy

from AriaQuanta.aqc.qubit import MultiQubit
from AriaQuanta.aqc.gatelibrary import Custom

from AriaQuanta._utils import np

class Circuit:
    def __init__(self, num_of_qubits, num_of_classical_bits=0):

        self.num_of_qubits = num_of_qubits
        self.gates = []

        self.width = num_of_qubits     # number of wires (qubits)
        #self.size:   # as a property  # number of gates
        #self.depth:  # as a property  # number of operations (independent gates)
        #self.data:   # as a property  # dictionary of everything
        
        multiqubit = MultiQubit(num_of_qubits)
        statevector = multiqubit.multistate    
        self.statevector = statevector

        self.size_of_matrix = 2**self.num_of_qubits
        self.density_matrix = np.empty([self.size_of_matrix, self.size_of_matrix])

        this_state = self.statevector
        density_matrix = this_state @ this_state.T
        self.density_matrix = density_matrix

    #----------------------------------------------
    @property
    def size(self):
        return len(self.gates)

    #----------------------------------------------
    @property
    def depth(self):
        return self.get_depth()

    #----------------------------------------------
    def get_depth(self):

        depth = 0
        if len(self.gates) > 0:
            depth += 1
            gates = self.gates
            qubits_i = gates[0].qubits
            qubits_previous = []

            qubits_previous = qubits_i

            for i in range(1, len(gates)):
                qubits_i = gates[i].qubits
                flag = np.in1d(qubits_i,qubits_previous).any()

                if flag:
                    depth += 1
                    qubits_previous = qubits_i
                else:
                    qubits_previous = np.concatenate((qubits_previous, qubits_i))                        

        return depth     
    
    #----------------------------------------------
    @property
    def data(self):
        dict_data = {}

        dict_data['depth'] = self.depth
        dict_data['gates'] = self.gates
        dict_data['num_of_qubits'] = self.num_of_qubits
        dict_data['size'] = self.size
        dict_data['statevector'] = self.statevector
        dict_data['width'] = self.width
        dict_data['density_matrix'] = self.density_matrix

        return dict_data

    #----------------------------------------------
    def __or__(self, gate):
        self.add_gate(gate)
        return self

    #----------------------------------------------
    def add_gate(self, gate):
        self.gates.append(gate)             
        
    #----------------------------------------------
    def run(self):
        #count=0
        for gate in self.gates:
            #print("------------------")
            #print("count =", count)
            #print("gate = ", gate)
            #count += 1
            state = gate.apply(self.num_of_qubits, self.statevector)
            self.statevector = state
        return state
        
    #----------------------------------------------
    def measure(self):
        state = self.statevector
        # print("measure state = ", state)
        probabilities = np.abs(state) ** 2
        probabilities /= np.sum(probabilities)  # Normalize probabilities to sum to 1
        probabilities = probabilities.flatten()
        measurement_index = np.random.choice(len(state), p=probabilities)
        
        num_of_states = np.shape(state)[0]
        num_of_qubits = int(np.log2(num_of_states))
        bin_format = '#0' + str(num_of_qubits + 2) + 'b'
        measurement_state = format(measurement_index, bin_format)[2:]
        measurement = '|' + measurement_state + '>'

        #-------------------------------------
        plt.rc('font', family='sans-serif')
        plt.rcParams['font.size']= 14
        plt.rcParams['axes.linewidth']= 1.5

        xtickes = []
        for i in range(num_of_states):
            bin_i =  format(i, bin_format)[2:]
            # print(bin_i)
            xtickes.append(bin_i)

        fig, ax = plt.subplots()
        xx = np.arange(np.shape(probabilities)[0])
        ax.bar(xx, probabilities)
        plt.xticks(xx, xtickes, rotation=45)
        ax.set_ylabel('Probability')
        #-------------------------------------        

        return measurement, measurement_index, probabilities 
    
        #----------------------------------------------
    def measure_qubit(self, quantum_bits, classical_bits):
 
        # example:
        # qc.measure([1, 2], [0, 1])
        # Measures qubit 1 into classical bit 0 and qubit 2 into classical bit 1

        qc_copy = self.copy()
        qc_copy.run()

        state = qc_copy.statevector
        #print("measure state = ", state)
        probabilities = np.abs(state) ** 2
        #print(probabilities)
        probabilities /= np.sum(probabilities)  # Normalize probabilities to sum to 1
        probabilities = probabilities.flatten()
        measurement_index = np.random.choice(len(state), p=probabilities)
        
        num_of_states = np.shape(state)[0]
        num_of_qubits = int(np.log2(num_of_states))
        bin_format = '#0' + str(num_of_qubits + 2) + 'b'
        measurement_state = format(measurement_index, bin_format)[2:]
        measurement = '|' + measurement_state + '>'
        #print(measurement)
        
        if len(quantum_bits) != len(classical_bits):
            raise("the measurement quantum and classincal inputs have to have the same length")
        
        classical_bits_values = {}
        for i in range(len(quantum_bits)):
            meausrement_i = measurement_state[quantum_bits[i]]
            classical_bits_values[str(classical_bits[i])] = int(meausrement_i)

        return classical_bits_values
            

        #-------------------------------------
        # plt.rc('font', family='sans-serif')
        # plt.rcParams['font.size']= 14
        # plt.rcParams['axes.linewidth']= 1.5

        # xtickes = []
        # for i in range(num_of_states):
        #    bin_i =  format(i, bin_format)[2:]
        #    # print(bin_i)
        #    xtickes.append(bin_i)

        # fig, ax = plt.subplots()
        # xx = np.arange(np.shape(probabilities)[0])
        # ax.bar(xx, probabilities)
        # plt.xticks(xx, xtickes, rotation=45)
        # ax.set_ylabel('Probability')
        #-------------------------------------  
        # 

    #----------------------------------------------
    def copy(self): 
        # num_of_qubits = self.num_of_qubits
        # gates = self.gates
        # statevector = self.statevector
        # density_matrix = self.density_matrix
        # this_qc = Circuit(num_of_qubits)
        # this_qc.gates = gates
        # this_qc.statevector = statevector
        # this_qc.density_matrix = density_matrix
        # print("this_qc.data: ", this_qc.data)  
        qc_copy = deepcopy(self)
        # print("qc_copy.data: ", qc_copy.data)
        return qc_copy

    #----------------------------------------------
    
   
def to_gate(qc):   # quantum circuit

    num_of_qubits = qc.num_of_qubits

    this_qc = Circuit(num_of_qubits)
    this_qc.gates = qc.gates

    # state_0
    state_0 = this_qc.statevector
    state_0_norm = state_0 / np.linalg.norm(state_0)
    #print(this_qc.data)
 
    # state_1
    state_1 = this_qc.run()
    #print(this_qc.data)
    state_1_norm = state_1 / np.linalg.norm(state_1)
    #print(this_qc.data)

    #------------
    # state_1 -> normalized last state
    # state_0 -> normalize initial state
    # v = state_1 - state_0
    # A = I - 2 (v v_dagger) / (v_dagger v)
    v = state_1_norm - state_0_norm
    v = np.reshape(v, (v.size, 1))
    v_dagger = np.reshape(v, (1, v.size))

    V_Vdagger = v @ v_dagger
    Vdagger_V = v_dagger @ v
    I = np.eye(2 ** num_of_qubits)

    A = I - 2 * V_Vdagger / Vdagger_V
    
    circuit_gate = Custom(matrix=A, target_qubits=list(range(0, num_of_qubits)))
    circuit_gate.matrix = A
    circuit_gate.name = 'Circuit_gate'

    return circuit_gate
    


