
import math
import matplotlib.pyplot as plt
from AriaQuanta._utils import np

#------------------------------------------------------------------------------------
class Result():
    def __init__(self, state_all):
        self.state_all = state_all
        self.iterations = len(self.state_all)
        
        # self.density_matrix_all

    #----------------------------------------------
    @property
    def density_matrix_all(self):
        return self.to_density_matrix()

    #----------------------------------------------    
    def to_density_matrix(self):
        density_matrix_all = []    
        for i in range(self.iterations):
            this_state = self.state_all[i]
            this_density_matrix = this_state @ this_state.T
            density_matrix_all.append(this_density_matrix)

        return density_matrix_all
    
    #----------------------------------------------
    def measure_one_state(self, state):

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
        
        return measurement, measurement_index, probabilities 


    #----------------------------------------------  
    def measure_and_count(self):

        num_of_qubits = int(math.log(len(self.state_all[0]), 2))
        size_of_statevector = self.state_all[0].shape[0]

        dict_counts = {}           
        for i in range(size_of_statevector):
            mystate_str = bin(i)[2:].zfill(num_of_qubits)
            dict_counts[mystate_str] = 0

        probabilities_all = []
        for i in range(self.iterations):  
            this_state = self.state_all[i]
            measurement, measurement_index, probabilities = self.measure_one_state(this_state) 
            
            mystate_str = measurement[1:-1]
            dict_counts[mystate_str] += 1   
            probabilities_all.append(probabilities)                 

        probabilities_counts = []
        for i in range(size_of_statevector):
            mystate_str = bin(i)[2:].zfill(num_of_qubits)
            probabilities_counts.append(dict_counts[mystate_str])

        probabilities_counts = np.array(probabilities_counts)    
        probabilities_counts = probabilities_counts / np.sum(probabilities_counts)
        
        measurement_result = {}
        measurement_result['counts'] = dict_counts
        measurement_result['probabilities_all'] = probabilities_all
        measurement_result['probabilities_counts'] = probabilities_counts


        return measurement_result
    
    #---------------------------------------------- 
    def plot_probability(self, probabilities):

        plt.rc('font', family='sans-serif')
        plt.rcParams['font.size']= 14
        plt.rcParams['axes.linewidth']= 1.5

        num_of_states = np.shape(probabilities)[0]
        num_of_qubits = int(np.log2(num_of_states))
        bin_format = '#0' + str(num_of_qubits + 2) + 'b'

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


class ResultDensity():
    def __init__(self, density_matrix_all):
        self.density_matrix_all = density_matrix_all