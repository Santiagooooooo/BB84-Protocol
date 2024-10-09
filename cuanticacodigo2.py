from qiskit import QuantumCircuit, Aer 
from qiskit.primitives import Sampler
import random

# Número de qubits (longitud de la clave)
num_qubits = 10

# Generación aleatoria de bits (clave inicial de Alice)
alice_bits = [random.randint(0, 1) for _ in range(num_qubits)]

# Elección aleatoria de las bases de Alice (0 = base Z, 1 = base X)
alice_bases = [random.randint(0, 1) for _ in range(num_qubits)]

# Elección aleatoria de las bases de Bob
bob_bases = [random.randint(0, 1) for _ in range(num_qubits)]

# Crear los qubits de Alice y medir con las bases de Bob
def bb84_circuit(alice_bits, alice_bases, bob_bases):
    circuit = QuantumCircuit(num_qubits, num_qubits)

    # Preparación de qubits de Alice
    for i in range(num_qubits):
        if alice_bits[i] == 1:
            circuit.x(i)
        if alice_bases[i] == 1:
            circuit.h(i)
    
    # Medición de los qubits en la base de Bob
    for i in range(num_qubits):
        if bob_bases[i] == 1:
            circuit.h(i)
        circuit.measure(i, i)
    
    return circuit

# Crear el circuito BB84
circuit = bb84_circuit(alice_bits, alice_bases, bob_bases)

# Simulador cuántico
backend = Aer.get_backend('qasm_simulator')

# Crear un sampler para ejecutar el circuito en el simulador
sampler = Sampler(backend)

# Ejecutar el circuito
result = sampler.run(circuit, shots=1)

# Resultados de la medición de Bob
bob_results = list(result.get_counts().keys())[0]

# Comparar las bases de Alice y Bob para generar la clave compartida
shared_key = [alice_bits[i] for i in range(num_qubits) if alice_bases[i] == bob_bases[i]]

# Mostrar los resultados
print("Bits de Alice:", alice_bits)
print("Bases de Alice:", alice_bases)
print("Bases de Bob:  ", bob_bases)
print("Resultados de Bob:", bob_results)
print("Clave compartida:", shared_key)
