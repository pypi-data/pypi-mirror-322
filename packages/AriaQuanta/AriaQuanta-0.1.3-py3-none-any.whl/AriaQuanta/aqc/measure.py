
import numpy as np

class Measure:

    def __init__(self, name, qubits, cbits):
        
        self.name = name
        self.qubits = qubits
        self.cbits = cbits
        self.qc_values = []
        self.c_values_dict = {}
        self.q_values_dict = {}


    def apply(self, num_of_qubits, multistate):

        # example:
        # qc.measure([1, 2], [0, 1])
        # Measures qubit 1 into classical bit 0 and qubit 2 into classical bit 1

        if self.cbits == []:
            for i in self.qubits:
                self.cbits = ['c'+str(i)]

        q_bits = self.qubits
        cbits = self.cbits            

        #---------------------------------------
        # measure
        state = multistate
        #print("measure state = ", state)
        probabilities = np.abs(state) ** 2
        #print(probabilities)
        probabilities /= np.sum(probabilities)  # Normalize probabilities to sum to 1
        probabilities = probabilities.flatten()
        measurement_index = np.random.choice(len(state), p=probabilities)
    
        num_of_states = np.shape(state)[0]
        num_of_qubits = int(np.log2(num_of_states))
        bin_format = '#0' + str(num_of_qubits + 2) + 'b' # #05b
        measurement_state = format(measurement_index, bin_format)[2:]  # 0b110
        measurement = '|' + measurement_state + '>'
        # print("measurement = ", measurement)
    
        if len(q_bits) != len(cbits):
            raise("the measurement quantum and classincal inputs have to have the same length")

        #---------------------------------------
        # save measurement outputs
        qc_values = []
        c_values_dict = {}
        q_values_dict = {}
        # qc_values: {'q_bit': value}
        # c_values_dict: {'c0': 1, 'c1': 1}
        for i in range(len(q_bits)):
            q_bits_i = q_bits[i]
            meausrement_i = measurement_state[q_bits_i]
            c_value = int(meausrement_i)
            qc_values.append((q_bits_i, str(cbits[i]), c_value))
            q_values_dict[str(q_bits_i)] = c_value
            c_values_dict[str(cbits[i])] = c_value


        self.qc_values = qc_values
        self.c_values_dict = c_values_dict
        self.q_values_dict = q_values_dict
        # print(qc_values, c_values_dict)

        #---------------------------------------
        # collapse the state

        all_states = [format(x, bin_format)[2:] for x in range(num_of_states)]

        select_indices = []
        for i in range(len(qc_values)):
            indices = [index for index, string in enumerate(all_states) if string[qc_values[i][0]] == str(qc_values[i][2])]
            select_indices.append(indices)
        # print('------')
        # print(select_indices)
        common_indices = list(set(select_indices[0]).intersection(*select_indices[1:]))
        # print(common_indices)
        all_indices = range(0, num_of_states)
        remove_indices = [num for num in all_indices if num not in common_indices]
        # print(remove_indices)
        
        multistate[remove_indices] = 0
        probabilities_selected = probabilities[common_indices]
        # print(probabilities_selected)  
        scale_probabilities = 1 / np.sum(probabilities_selected)   
        # print(scale_probabilities)  
        scale_probabilities_sqrt = np.sqrt(scale_probabilities)
        multistate[common_indices] *= scale_probabilities_sqrt

        return multistate

class MeasureQubit(Measure):
    def __init__(self, qubits, cbits=[]):            
        super().__init__(name='MeasureQubit', qubits=qubits, cbits=cbits)


