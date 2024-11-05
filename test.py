import streamlit as st
import numpy as np

def create_sudoku_grid():
    """Initialize an empty Sudoku grid."""
    return np.zeros((9, 9), dtype=int)

def display_sudoku_grid(grid):
    """Display the Sudoku grid in a structured format with reduced spacing."""
    for i in range(9):
        # Create a row with 9 columns
        cols = st.columns(9, gap="small")  # Create 9 columns with small gaps for each row
        for j in range(9):
            if grid[i][j] == 0:
                # Allow input only for empty cells
                value = cols[j].text_input(
                    '', 
                    key=f'{i}-{j}', 
                    max_chars=1, 
                    placeholder=' ',
                    label_visibility="collapsed",
                    help="Enter a number between 1-9"
                )
                if value.isdigit() and 1 <= int(value) <= 9:
                    grid[i][j] = int(value)
            else:
                # Show pre-filled numbers
                cols[j].markdown(
                    f"<div style='height: 50px; width: 50px; font-size: 24px; text-align: center; margin: 0; padding: 0; border: 1px solid black;'>"
                    f"{grid[i][j]}</div>", 
                    unsafe_allow_html=True
                )

def is_valid(num, row, col, grid):
    """Check if a number can be placed in the specified cell."""
    for x in range(9):
        if grid[row][x] == num or grid[x][col] == num:
            return False
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if grid[i][j] == num:
                return False
    return True

def solve_sudoku(grid):
    """Solve the Sudoku using a backtracking algorithm."""
    def solve():
        for i in range(9):
            for j in range(9):
                if grid[i][j] == 0:
                    for num in range(1, 10):
                        if is_valid(num, i, j, grid):
                            grid[i][j] = num
                            if solve():
                                return True
                            grid[i][j] = 0
                    return False
        return True

    solve()
    return grid

# Initialize an empty Sudoku grid
initial_grid = create_sudoku_grid()

st.title("SudokuMaster")
st.subheader("Interactive Sudoku Game")

# Display the Sudoku grid
display_sudoku_grid(initial_grid)

if st.button("Solve"):
    # Read user inputs and populate the grid
    for i in range(9):
        for j in range(9):
            input_value = st.session_state.get(f'{i}-{j}', '')
            initial_grid[i][j] = int(input_value) if input_value.isdigit() and 1 <= int(input_value) <= 9 else 0
    
    solved_grid = solve_sudoku(initial_grid)

    st.subheader("Solved Sudoku:")
    display_sudoku_grid(solved_grid)
