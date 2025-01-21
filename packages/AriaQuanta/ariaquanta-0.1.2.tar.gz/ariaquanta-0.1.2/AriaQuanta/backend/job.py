
from AriaQuanta.aqc.circuit import Circuit
from AriaQuanta._utils import np

#------------------------------------------------------------------------------------
class Job():
    def __init__(self, job_id):
        self.job_id = job_id
        self.status = 'Job %s not yet started'.format(self.job_id)

    def job_run(self, circuit, density):

        self.status = 'Job {} started'.format(self.job_id)
        
        if self.job_id % 50 == 0:
            print(self.status)

        num_of_qubits = circuit.num_of_qubits
        this_qc = Circuit(num_of_qubits)
        this_qc.gates = circuit.gates
        state = this_qc.statevector
        this_qc.density_matrix = circuit.density_matrix

        if density == False:
            for gate in this_qc.gates:
                state = gate.apply(this_qc.num_of_qubits, this_qc.statevector)

                # Apply noise
                #if this_qc.noise_type:
                #    state = this_qc.noise_type.apply_noise(this_qc.num_of_qubits, this_qc.statevector, density)

                this_qc.statevector = state

        elif density == True:
            for gate in this_qc.gates:
                state = gate.apply_density(this_qc.num_of_qubits, this_qc.density_matrix)

                this_qc.density_matrix = state
  

        self.status = 'Job {} completed'.format(self.job_id)

        if self.job_id % 50 == 0:
            print(self.status) 
                   
        return state  
        
        
        
