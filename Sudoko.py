import sys
import csv
import time

class SudokuSolver:
    nodes_generated = 0

    def __init__(self, puzzle):
        self.puzzle = puzzle
        self.n = len(puzzle)
        self.sqrt_n = int(self.n ** 0.5)
        self.valid_set = set(str(i) for i in range(1, self.n + 1))
        # self.nodes_generated = 0

    def print_puzzle(self):
        for row in self.puzzle:
            print(",".join(str(val) if val else 'X' for val in row))

    def save_solution(self, filename):
        filename_without_extension = filename.split('.')[0]  # Get the part before '.csv'
        with open(f"{filename_without_extension}_solution.csv", 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(self.puzzle)

    def is_valid(self, row, col, num):
        for i in range(self.n):
            if self.puzzle[row][i] == num and i != col:
                return False  # Return False if num is found in the same row (except the current column)
            if self.puzzle[i][col] == num and i != row:
                return False  # Return False if num is found in the same column (except the current row)

        # Determine the start indices of the 3x3 subgrid
        start_row, start_col = self.sqrt_n * (row // self.sqrt_n), self.sqrt_n * (col // self.sqrt_n)
        
        # Check the 3x3 subgrid for the given number
        for i in range(self.sqrt_n):
            for j in range(self.sqrt_n):
                if self.puzzle[i + start_row][j + start_col] == num and (i + start_row != row or j + start_col != col):
                    return False  # Return False if num is found in the 3x3 subgrid (except the current cell)
        
        return True

        start_row, start_col = self.sqrt_n * (row // self.sqrt_n), self.sqrt_n * (col // self.sqrt_n)
        for i in range(self.sqrt_n):
            for j in range(self.sqrt_n):
                if self.puzzle[i + start_row][j + start_col] == num:
                    return False
        return True

    def find_empty_location(self):
        min_values = float('inf')
        min_location = None
        for i in range(self.n):
            for j in range(self.n):
                if self.puzzle[i][j] == 0:
                    valid_values = self.valid_set - set(
                        str(self.puzzle[i][k]) for k in range(self.n) if self.puzzle[i][k] != 0
                    )
                    valid_values -= set(
                        str(self.puzzle[k][j]) for k in range(self.n) if self.puzzle[k][j] != 0
                    )
                    start_row, start_col = self.sqrt_n * (i // self.sqrt_n), self.sqrt_n * (j // self.sqrt_n)
                    valid_values -= set(
                        str(self.puzzle[r][c])
                        for r in range(start_row, start_row + self.sqrt_n)
                        for c in range(start_col, start_col + self.sqrt_n)
                        if self.puzzle[r][c] != 0
                    )
                    num_values = len(valid_values)
                    if num_values < min_values:
                        min_values = num_values
                        min_location = (i, j)
        return min_location

    def count_nodes(self):
        self.nodes_generated += 1

    def solve_brute_force(self):
        def recursive_solver():
            find = self.find_empty_location()
            if not find:
                return True
            row, col = find

            for num in self.valid_set:
                SudokuSolver.nodes_generated += 1
                if self.is_valid(row, col, num):
                    self.puzzle[row][col] = int(num)
                    if recursive_solver():
                        return True
                    self.puzzle[row][col] = 0

            return False

        SudokuSolver.nodes_generated = 0
        if recursive_solver():
            return True
        return False
    
    def solve_backtracking(self):
        def recursive_solver():
            find = self.find_empty_location()
            if not find:
                return True
            row, col = find

            for num in self.valid_set:
                SudokuSolver.nodes_generated += 1
                if self.is_valid(row, col, num):
                    self.puzzle[row][col] = int(num)
                    if recursive_solver():
                        return True
                    self.puzzle[row][col] = 0

            return False

        SudokuSolver.nodes_generated += 0
        if recursive_solver():
            return True
        return False
    
    def solve_forward_checking(self):
        def recursive_solver():
            find = self.find_empty_location()
            if not find:
                return True
            row, col = find

            valid_values = self.valid_set - set(
                str(self.puzzle[row][k]) for k in range(self.n) if self.puzzle[row][k] != 0
            )
            valid_values -= set(
                str(self.puzzle[k][col]) for k in range(self.n) if self.puzzle[k][col] != 0
            )
            start_row, start_col = self.sqrt_n * (row // self.sqrt_n), self.sqrt_n * (col // self.sqrt_n)
            valid_values -= set(
                str(self.puzzle[r][c])
                for r in range(start_row, start_row + self.sqrt_n)
                for c in range(start_col, start_col + self.sqrt_n)
                if self.puzzle[r][c] != 0
            )

            for num in valid_values:
                SudokuSolver.nodes_generated += 1
                self.puzzle[row][col] = int(num)
                if recursive_solver():
                    return True
                self.puzzle[row][col] = 0

            return False

        SudokuSolver.nodes_generated += 0
        if recursive_solver():
            return True
        return False

    def solve(self, mode):
        if mode == 1:  # Brute force search
            self.nodes_generated = 0  # Reset counter before solving
            start_time = time.time()
            solved = self.solve_brute_force()
            end_time = time.time()
            algo_name = 'Brute Force Search'

        elif mode == 2:  # Backtracking
            self.nodes_generated = 0  # Reset counter before solving
            start_time = time.time()
            solved = self.solve_backtracking()
            end_time = time.time()
            algo_name = 'Backtracking Search'

        elif mode == 3:  # CSP with forward-checking and MRV heuristic
            self.nodes_generated = 0  # Reset counter before solving
            start_time = time.time()
            solved = self.solve_forward_checking()
            end_time = time.time()
            algo_name = 'CSP with Forward Checking and MRV Heuristic'
        else:
            print("Invalid mode selected.")
            return

        if not solved:
            print("No solution exists.")
            return

        search_time = end_time - start_time
        print(f"Input puzzle:")
        self.print_puzzle()
        # print(f"\nNumber of search tree nodes generated: 0")  # For simplicity, not counting nodes
        print(f"Search time: {search_time:.6f} seconds")

        print("\nSolved puzzle:")
        self.print_puzzle()

        if mode != 4:
            self.save_solution(f"{sys.argv[2]}_solution.csv")

    def validate_solution(self):
        for i in range(self.n):
            for j in range(self.n):
                if not self.is_valid(i, j, self.puzzle[i][j]):
                    return False
        return True

def load_sudoku_from_csv(filename):
    try:
        with open(filename, newline='', encoding='utf-8-sig') as csvfile:  # Specify the encoding to handle BOM
            sudoku_reader = csv.reader(csvfile)
            puzzle = [[int(val) if val != 'X' else 0 for val in row] for row in sudoku_reader]
            return puzzle
    except FileNotFoundError:
        print("ERROR: Input file not found.")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("ERROR: Not enough/too many input arguments.")
        sys.exit(1)

    mode = int(sys.argv[1])
    filename = sys.argv[2]

    puzzle = load_sudoku_from_csv(filename)
    sudoku_solver = SudokuSolver(puzzle)

    if mode == 4:
        is_valid_solution = sudoku_solver.validate_solution()
        print("Last Name, First Name, AXXXXXXXX solution:")
        print(f"Input file: {filename}")
        print("Algorithm: TEST")

        sudoku_solver.print_puzzle()
        if is_valid_solution:
            print("\nThis is a valid, solved Sudoku puzzle.")
        else:
            print("\nERROR: This is NOT a solved Sudoku puzzle.")
    else:
        sudoku_solver.solve(mode)
        print(f"Last Name: XYZ, First Name: ABC, AXXXXXXXX solution:")
        print(f"Input file: {filename}")
        if mode == 1:
            algo_name = 'Brute Force Search'
        elif mode == 2:
            algo_name = 'Backtracking Search'
        elif mode == 3:
            algo_name = 'CSP with Forward Checking and MRV Heuristic'
        else:
            algo_name = 'Invalid Algorithm'

        print(f"Algorithm: {algo_name}")
