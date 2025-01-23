

class Operations:

    def __init__(self, name, condition, operation_gate):
        
        self.name = name  
        self.condition = condition
        self.operation_gate = operation_gate

    def apply(self, num_of_qubits, multistate):

        # print("multistate1", multistate)
        this_gate = self.operation_gate
        multistate = this_gate.apply(num_of_qubits, multistate)
        # print(this_gate.target_qubit)
        # print("multistate2", multistate)
        return multistate

#------------------------------------------------------------------------------------
class If_cbit(Operations):
    def __init__(self, condition, operation_gate):
        super().__init__(name='If_cbit', condition=condition, operation_gate=operation_gate)
    
