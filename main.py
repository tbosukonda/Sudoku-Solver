import streamlit as st
from collections import defaultdict

st.markdown(
    """
    <div style="text-align: center;">
        <h2>SUDOKU SOLVER</h2>
    </div>
    """, 
    unsafe_allow_html=True
)
st.markdown(
    """
    <div style="text-align: center;">
        Instructions: Enter your initial sudoku layout. For blank spaces enter 0.
    </div>
    """, 
    unsafe_allow_html=True
)
st.markdown(
    """
    <style>
    div.stButton > button {
        display: block;
        margin-left: auto;
        margin-right: auto;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown(
    """
    <style>
    div.stAlert {
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

def solve_sudoku(board):

    row_nums = defaultdict(list)
    col_nums = defaultdict(list)
    block_nums = defaultdict(list)

    ROW, COL = len(board), len(board[0])

    # Populating the initial placement
    for i in range(ROW):
        for j in range(COL):
            if board[i][j] != 0:
                num = board[i][j] 
                row_nums[i].append(num)
                col_nums[j].append(num)
                block_nums[(i//3, j//3)].append(num)

    def backtrack(i, j):
        # Reached the last cell
        if i == 8 and j == 9:
            return True

        # Reached the last column in a row, move to the next row
        if j == 9:
            i += 1
            j = 0

        # The cell has a digit already
        if board[i][j] != 0:
            return backtrack(i, j+1)
        
        # The cell is not filled
        for n in range(1, 10):
            # If the number is already used in the row, column, or block, skip it
            if n in row_nums[i] or n in col_nums[j] or n in block_nums[(i//3, j//3)]:
                continue

            board[i][j] = n
            row_nums[i].append(n)
            col_nums[j].append(n)
            block_nums[(i//3, j//3)].append(n)

            if backtrack(i, j+1):
                return True

            board[i][j] = 0
            row_nums[i].remove(n)
            col_nums[j].remove(n)
            block_nums[(i//3, j//3)].remove(n)

        return False

    return backtrack(0, 0):

def display_grid():
    grid = []
    
    for i in range(9):
        row = []
        
        if i in [3, 6]:  # Add a horizontal spacer after every 3 rows
            st.write("")  # Adding a blank row for spacing
        
        cols = st.columns([0.75, 0.75, 0.75, 0.5, 0.75, 0.75, 0.75, 0.5, 0.75, 0.75, 0.75])  # Adjusting column widths with spaces
        
        for j in range(9):
            row.append(int(cols[j + (j // 3)].text_input('', value="0", max_chars=1, key=f'{i}{j}')))
        
        grid.append(row)
    return grid

def display_solved_grid(grid):
    
    for i in range(9):
        row = []
        
        if i in [3, 6]:  
            st.write("")
        
        cols = st.columns([0.75, 0.75, 0.75, 0.5, 0.75, 0.75, 0.75, 0.5, 0.75, 0.75, 0.75])
        
        for j in range(9):
            row.append(int(cols[j + (j // 3)].text_input('', value=grid_copy[i][j], max_chars=1, key=f'solved_{i}{j}')))
                 
        grid.append(row)

grid = display_grid()

if st.button('Solve'):

    grid_copy = [row[:] for row in grid]  

    if solve_sudoku(grid_copy):
        st.success("Sudoku solved!")
        display_solved_grid(grid_copy)
    else:
        st.error("No solution exists for the given Sudoku.")