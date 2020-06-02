# First test circuit creates 3-qubit GHZ state

from qiskit import *
from qiskit.visualization import plot_state_city, plot_histogram

# Create quantum circuit from 3 quantum registers
circ = QuantumCircuit(3, 3)

# For this example I am going to run this circuit on the Qiskit Statevector simulator
backend = Aer.get_backend('statevector_simulator')

# Add H gate to first register, placing 1st qubit in equal superpostion
circ.h(0)

# Add CNOT gate on control qubit 0 and target qubit 1 to place qubits 1 and 2 in bell state
circ.cx(0, 1)

# Add CNOT gate on control qubit 0 and target qubit 3 to create GHZ state
circ.cx(0, 2)

# Creating a barrier to delimninate state prepartaion from measurement
circ.barrier(range(3))

circ.draw(output='mpl', filename='ghz_images/ghz_quantum_circuit.png')

# Now let's plot the density matrix of our GHZ state
# Note that if you are using an IDE like pycharm, then plot_state_city will not display any results
# I will include in a later more complete jupyter noteboook how to view plot_state_city in an IDE
# For now, my results are summarized in ghz_density_matrix
quantum_job = execute(circ, backend)
result = quantum_job.result()
ghz_state = result.get_statevector(circ, decimals=3)
plot_state_city(ghz_state)


# Creating a measurement circuit to map our quantum state to a classical output
meas = QuantumCircuit(3, 3)

meas.measure(range(3), range(3))

meas.draw(output='mpl')

# Combing quantum and measurement circuits
ghz_circuit = circ + meas

ghz_circuit.draw(output='mpl')

# To simulate the behavior of our full GHZ circuit we will use qiskit Aer's QASM simulator

backend_sim = Aer.get_backend('qasm_simulator')
ghz_sim = execute(ghz_circuit, backend_sim, shots=1024)
ghz_results = ghz_sim.result()

# The classical outputs of this circuit are summarized with counts
counts = ghz_results.get_counts()
print(counts)

# Counts are summarized in a rather boring histogram, which again won't display with an IDE
# My results are summarized in counts_histogram.png
plot_histogram(counts)

