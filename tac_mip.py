import sys

class TACtoMIPSConverter:
    def __init__(self):
        self.mips_code = []
        self.data_section = []
        self.current_method = None
        self.current_class = None
        self.label_counter = 0

    def generate_label(self):
        label = f"label_{self.label_counter}"
        self.label_counter += 1
        return label

    def convert_tac_to_mips(self, tac_code):
        self.mips_code.append(".data")
        self.mips_code.extend(self.data_section)

        self.mips_code.append("\n.text")

        for line in tac_code:
            tokens = line.split()

            if not tokens or len(tokens) < 2:
                continue  # Skip empty lines or lines without enough tokens

            if tokens[0] == "class":
                self.current_class = tokens[1]
                self.current_method = None
                continue

            elif tokens[0] == "declare":
                self.data_section.append(f"{self.current_class}_{tokens[1]}: .space 4")  # Assume variables are 4 bytes

            elif tokens[0].startswith("method"):
                self.current_method = tokens[0]
                self.mips_code.append(f"\n{self.current_class}_{self.current_method}:")

            elif tokens[0] == "return":
                if tokens[1] == "void":
                    self.mips_code.append("jr $ra")  # Return void (jump back to nothing)
                else:
                    self.mips_code.append(f"li $v0, {tokens[1]}")  # Load immediate value to register
                    self.mips_code.append("jr $ra")  # Jump back to the calling function

            elif tokens[0] == "call" and len(tokens) >= 2:
                called_method_parts = tokens[1].split('.')
                if len(called_method_parts) >= 2:
                    called_class = called_method_parts[0]
                    called_method = called_method_parts[1]
                    self.mips_code.append(f"jal {called_class}_{called_method}")

            elif len(tokens) >= 3 and tokens[1] == "=":
                # Handle assignments
                if tokens[2].isdigit():
                    # If the right-hand side is a constant
                    self.mips_code.append(f"li $t0, {tokens[2]}")  # Load immediate value to register
                elif tokens[2].startswith("_t"):
                    # If the right-hand side is a temporary variable
                    self.mips_code.append(f"lw $t0, {self.current_class}_{tokens[2]}")  # Load value from variable
                else:
                    # If the right-hand side is a variable
                    self.mips_code.append(f"lw $t0, {self.current_class}_{tokens[2]}")  # Load value from variable

                # Store in the left-hand side variable
                self.mips_code.append(f"sw $t0, {self.current_class}_{tokens[0]}")

            elif len(tokens) >= 5 and tokens[3] in ("+", "-", "*", "/"):
                # Handle basic arithmetic operations
                self.mips_code.append(f"lw $t0, {self.current_class}_{tokens[2]}")  # Load value of the first operand
                self.mips_code.append(f"lw $t1, {self.current_class}_{tokens[4]}")  # Load value of the second operand

                if tokens[3] == "+":
                    self.mips_code.append("add $t2, $t0, $t1")  # Addition
                elif tokens[3] == "-":
                    self.mips_code.append("sub $t2, $t0, $t1")  # Subtraction
                elif tokens[3] == "*":
                    self.mips_code.append("mul $t2, $t0, $t1")  # Multiplication
                elif tokens[3] == "/":
                    self.mips_code.append("div $t0, $t1")  # Division
                    self.mips_code.append("mflo $t2")  # Move quotient to $t2

                # Store the result in the destination variable
                self.mips_code.append(f"sw $t2, {self.current_class}_{tokens[0]}")

            elif len(tokens) >= 4 and tokens[2] in (">", "<", "==", "!="):
                # Handle comparison operations
                label_true = self.generate_label()
                label_end = self.generate_label()

                self.mips_code.append(f"lw $t0, {self.current_class}_{tokens[1]}")  # Load the first operand
                self.mips_code.append(f"lw $t1, {self.current_class}_{tokens[3]}")  # Load the second operand

                if tokens[2] == ">":
                    self.mips_code.append(f"bgt $t0, $t1, {label_true}")
                elif tokens[2] == "<":
                    self.mips_code.append(f"blt $t0, $t1, {label_true}")
                elif tokens[2] == "==":
                    self.mips_code.append(f"beq $t0, $t1, {label_true}")
                elif tokens[2] == "!=":
                    self.mips_code.append(f"bne $t0, $t1, {label_true}")

                self.mips_code.append(f"li $t2, 0")  # False case
                self.mips_code.append(f"j {label_end}")
                self.mips_code.append(f"{label_true}:")
                self.mips_code.append(f"li $t2, 1")  # True case
                self.mips_code.append(f"{label_end}:")

                # Store the result in the destination variable
                self.mips_code.append(f"sw $t2, {self.current_class}_{tokens[0]}")

    def get_mips_code(self):
        return "\n".join(self.data_section + self.mips_code)


def read_tac_file(file_path):
    with open(file_path, "r") as file:
        tac_code = file.readlines()
    return [line.strip() for line in tac_code]


def write_mips_file(mips_code, output_file_path):
    with open(output_file_path, "w") as file:
        file.write(mips_code)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python tac_to_mips.py input_tac_file output_mips_file")
        sys.exit(1)

    input_tac_file = sys.argv[1]
    output_mips_file = sys.argv[2]

    # Read TAC code from file
    tac_code = read_tac_file(input_tac_file)

    # Create the TAC to MIPS converter
    converter = TACtoMIPSConverter()

    # Convert TAC to MIPS
    converter.convert_tac_to_mips(tac_code)

    # Get the generated MIPS code
    mips_code = converter.get_mips_code()

    # Write MIPS code to output file
    write_mips_file(mips_code, output_mips_file)

    print(f"Conversion successful. MIPS code written to {output_mips_file}")
