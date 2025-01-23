import cirq
import numpy as np
import logging
import matplotlib.pyplot as plt

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class Zeeq:
    def __init__(self):
        self.circuit = cirq.Circuit()
        self.qubits = []
        self.simulator = cirq.Simulator()

    def interpret(self, command):
        """Interprets natural language commands for quantum circuit operations."""
        command = command.lower()

        try:
            if "create a circuit" in command:
                self.create_circuit(command)
            elif "add classical register" in command:
                logging.warning("Cirq does not use classical registers explicitly.")
            elif "initialize state" in command:
                self.initialize_state(command)
            elif "apply" in command and "gate" in command:
                self.apply_gate(command)
            elif "entangle qubits" in command:
                self.entangle_qubits(command)
            elif "apply qft" in command:
                self.apply_qft()
            elif "reset qubit" in command:
                self.reset_qubit(command)
            elif "add barrier" in command:
                logging.warning("Barriers are not used in Cirq.")
            elif "display the circuit" in command:
                self.display_circuit()
            elif "export the circuit" in command:
                self.export_circuit(command)
            elif "measure" in command:
                self.measure_qubits(command)
            elif "run the circuit" in command:
                self.run_circuit(command)
            elif "draw bloch sphere" in command:
                self.draw_bloch_sphere(command)
            elif "show the state vector" in command:
                self.display_state_vector()
            elif "show the density matrix" in command:
                self.display_density_matrix()
            elif "help" in command:
                self.display_help()
            else:
                logging.warning("Command not recognized.")
        except Exception as e:
            logging.error(f"Error interpreting command: {command}. Details: {e}")

    def create_circuit(self, command):
        """Create a quantum circuit with a specified number of qubits."""
        try:
            num_qubits = int(command.split("with")[1].split("qubits")[0].strip())
            self.qubits = [cirq.LineQubit(i) for i in range(num_qubits)]
            self.circuit = cirq.Circuit()
            logging.info(f"Quantum circuit with {num_qubits} qubits created.")
        except (ValueError, IndexError):
            logging.error("Invalid command for creating a circuit. Specify the number of qubits.")

    def initialize_state(self, command):
        """Initialize the state of the qubits."""
        try:
            state_vector = [complex(float(x)) for x in command.split("to state")[1].strip().split()]
            if len(state_vector) != 2 ** len(self.qubits):
                logging.error("State vector dimension does not match the number of qubits.")
                return
            init_gate = cirq.StatePreparationChannel(state_vector)
            self.circuit.append(init_gate(*self.qubits))
            logging.info(f"Qubits initialized to state {state_vector}.")
        except Exception as e:
            logging.error(f"Error initializing state: {e}")

    def apply_gate(self, command):
        """Apply quantum gates based on the command."""
        try:
            if "hadamard" in command:
                qubit = self.extract_qubit_index(command)
                self.circuit.append(cirq.H(self.qubits[qubit]))
                logging.info(f"Hadamard gate applied to qubit {qubit}.")
            elif "x gate" in command:
                qubit = self.extract_qubit_index(command)
                self.circuit.append(cirq.X(self.qubits[qubit]))
                logging.info(f"X gate applied to qubit {qubit}.")
            elif "rx gate" in command:
                angle, qubit = self.extract_angle_and_qubit(command, "rx gate")
                self.circuit.append(cirq.rx(angle)(self.qubits[qubit]))
                logging.info(f"RX gate with angle {angle} applied to qubit {qubit}.")
            elif "ry gate" in command:
                angle, qubit = self.extract_angle_and_qubit(command, "ry gate")
                self.circuit.append(cirq.ry(angle)(self.qubits[qubit]))
                logging.info(f"RY gate with angle {angle} applied to qubit {qubit}.")
            elif "rz gate" in command:
                angle, qubit = self.extract_angle_and_qubit(command, "rz gate")
                self.circuit.append(cirq.rz(angle)(self.qubits[qubit]))
                logging.info(f"RZ gate with angle {angle} applied to qubit {qubit}.")
            elif "cnot gate" in command:
                control, target = map(int, command.split("from qubit")[1].split("to qubit"))
                self.circuit.append(cirq.CNOT(self.qubits[control], self.qubits[target]))
                logging.info(f"CNOT gate applied from qubit {control} to qubit {target}.")
            else:
                logging.warning("Gate command not recognized.")
        except Exception as e:
            logging.error(f"Error applying gate: {e}")

    def entangle_qubits(self, command):
        """Entangle specified qubits."""
        try:
            qubits = list(map(int, command.split("entangle qubits")[1].strip().split()))
            if len(qubits) < 2:
                logging.error("Entanglement requires at least two qubits.")
                return
            self.circuit.append(cirq.H(self.qubits[qubits[0]]))
            for i in range(1, len(qubits)):
                self.circuit.append(cirq.CNOT(self.qubits[qubits[0]], self.qubits[qubits[i]]))
            logging.info(f"Qubits {qubits} entangled.")
        except Exception as e:
            logging.error(f"Error entangling qubits: {e}")

    def apply_qft(self):
        """Apply Quantum Fourier Transform to all qubits."""
        try:
            for i in range(len(self.qubits)):
                self.circuit.append(cirq.H(self.qubits[i]))
                for j in range(i + 1, len(self.qubits)):
                    angle = np.pi / (2 ** (j - i))
                    self.circuit.append(cirq.CZ(self.qubits[j], self.qubits[i]) ** (angle / np.pi))
            logging.info("Quantum Fourier Transform applied to all qubits.")
        except Exception as e:
            logging.error(f"Error applying QFT: {e}")

    def reset_qubit(self, command):
        """Reset specific or all qubits."""
        try:
            if "all qubits" in command:
                self.circuit.append(cirq.ResetChannel().on_each(*self.qubits))
                logging.info("All qubits have been reset.")
            else:
                qubit = self.extract_qubit_index(command)
                self.circuit.append(cirq.ResetChannel().on(self.qubits[qubit]))
                logging.info(f"Qubit {qubit} has been reset.")
        except Exception as e:
            logging.error(f"Error resetting qubit: {e}")

    def display_state_vector(self):
        """Display the state vector of the circuit."""
        try:
            result = self.simulator.simulate(self.circuit)
            logging.info(f"State vector: {result.final_state_vector}")
            print(result.final_state_vector)
        except Exception as e:
            logging.error(f"Error displaying state vector: {e}")

    def display_density_matrix(self):
        """Display the density matrix of the circuit."""
        try:
            result = self.simulator.simulate(self.circuit)
            density_matrix = cirq.density_matrix_from_state_vector(result.final_state_vector, num_qubits=len(self.qubits))
            logging.info(f"Density matrix:\n{density_matrix}")
            print(density_matrix)
        except Exception as e:
            logging.error(f"Error displaying density matrix: {e}")

    def display_circuit(self):
        """Display the current quantum circuit."""
        if self.circuit:
            print(self.circuit)
        else:
            logging.warning("No circuit has been created yet.")

    def export_circuit(self, command):
        """Export the circuit to a file."""
        try:
            filename = command.split("to file")[1].strip()
            if not filename.endswith(".txt"):
                filename += ".txt"
            with open(filename, "w") as f:
                f.write(str(self.circuit))
            logging.info(f"Circuit exported to {filename}.")
        except Exception as e:
            logging.error(f"Error exporting circuit: {e}")

    def measure_qubits(self, command):
        """Measure specified or all qubits."""
        try:
            if "all" in command:
                self.circuit.append(cirq.measure(*self.qubits))
                logging.info("Measured all qubits.")
            else:
                qubit = self.extract_qubit_index(command)
                self.circuit.append(cirq.measure(self.qubits[qubit]))
                logging.info(f"Measured qubit {qubit}.")
        except Exception as e:
            logging.error(f"Error measuring qubits: {e}")

    def draw_bloch_sphere(self, command):
        """Draw the Bloch sphere representation of a qubit."""
        try:
            qubit = self.extract_qubit_index(command)
            result = self.simulator.simulate(self.circuit)
            bloch_vector = cirq.bloch_vector_from_state_vector(result.final_state_vector, qubit)
            logging.info(f"Bloch sphere vector for qubit {qubit}: {bloch_vector}.")
            # Plotting Bloch sphere using matplotlib
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            ax.quiver(0, 0, 0, bloch_vector[0], bloch_vector[1], bloch_vector[2])
            ax.set_xlim([-1, 1])
            ax.set_ylim([-1, 1])
            ax.set_zlim([-1, 1])
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Z')
            plt.show()
        except Exception as e:
            logging.error(f"Error drawing Bloch sphere: {e}")

    def run_circuit(self, command):
        """Run the circuit with the specified number of repetitions."""
        try:
            shots = int(command.split("run the circuit")[1].split("times")[0].strip())
            result = self.simulator.run(self.circuit, repetitions=shots)
            logging.info(f"Execution result: {result}")
            print(result)
        except Exception as e:
            logging.error(f"Error running circuit: {e}")

    def display_help(self):
        """Display help information."""
        print("""
        Available commands:
        - Create a circuit with <N> qubits.
        - Initialize state to <state vector>.
        - Apply Hadamard gate to qubit <N>.
        - Apply X gate to qubit <N>.
        - Apply RX gate <angle> to qubit <N>.
        - Apply RY gate <angle> to qubit <N>.
        - Apply RZ gate <angle> to qubit <N>.
        - Apply CNOT gate from qubit <control> to qubit <target>.
        - Entangle qubits <N1> <N2> ...
        - Apply QFT to all qubits.
        - Reset qubit <N> or reset all qubits.
        - Measure qubit <N> or measure all qubits.
        - Display the circuit.
        - Export the circuit to file <filename>.
        - Show the state vector.
        - Show the density matrix.
        - Run the circuit <N> times.
        - Draw Bloch sphere for qubit <N>.
        """)

    def extract_qubit_index(self, command):
        """Helper function to extract a qubit index from a command."""
        return int(command.split("qubit")[1].strip())

    def extract_angle_and_qubit(self, command, gate):
        """Helper function to extract angle and qubit index from a gate command."""
        parts = command.split(gate)[1].split("to qubit")
        angle = float(parts[0].strip())
        qubit = int(parts[1].strip())
        return angle, qubit
