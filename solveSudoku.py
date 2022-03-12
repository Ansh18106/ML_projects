# User function Template for python3

class Solution:

    # Function to print grids of the Sudoku.
    def printGrid(self, arr):
        for i in range(9):
            for j in range(9):
                print(arr[i][j], end=" ")

    # Function to return a boolean which indicates whether an assigned
    # entry in the specified row matches the given number.
    def used_in_row(self, arr, row, num):
        for i in range(9):
            if (arr[row][i] == num):
                return True
        return False

    # Function to return a boolean which indicates whether an assigned
    # entry in the specified column matches the given number.
    def used_in_col(self, arr, col, num):
        for i in range(9):
            if (arr[i][col] == num):
                return True
        return False

    # Function to return a boolean which indicates whether an assigned
    # entry within the specified 3x3 box matches the given number.
    def used_in_box(self, arr, row, col, num):
        for i in range(3):
            for j in range(3):
                if (arr[i + row][j + col] == num):
                    return True
        return False

    # Function to return a boolean which indicates whether it will be
    # legal to assign num to the given row, column location.
    def check_location_is_safe(self, arr, row, col, num):
        return not self.used_in_row(arr, row, num) and not self.used_in_col(arr, col, num) and not self.used_in_box(arr,
                                                                                                                    row - row % 3,
                                                                                                                    col - col % 3,
                                                                                                                    num)

    def find_empty_location(self, arr, l):
        for row in range(9):
            for col in range(9):
                if (arr[row][col] == 0):
                    l[0] = row
                    l[1] = col
                    return True
        return False

    # Function to find a solved Sudoku.
    def SolveSudoku(self, grid):

        l = [0, 0]

        # if there is no unassigned location, we are done.
        if (not self.find_empty_location(grid, l)):
            return True

        row = l[0]
        col = l[1]

        # considering digits from 1 to 9
        for num in range(1, 10):

            if (self.check_location_is_safe(grid, row, col, num)):

                # making tentative assignment
                grid[row][col] = num
                # if success, return true
                if (self.SolveSudoku(grid)):
                    return True
                # failure, unmake & try again
                grid[row][col] = 0

        # this triggers backtracking
        return False


def solveSudoku(grid):
    ob = Solution()

    if (ob.SolveSudoku(grid)):
        for i in range(9):
            for j in range(9):
                print (grid[i][j], end = " ")
            print('||')
    else:
        print ('NOT A VALID SUDOKU')
    return grid



grid = [[0, 0, 0, 0, 9, 0, 0, 2, 0],
        [4, 0, 2, 5, 0, 0, 0, 6, 0],
        [0, 5, 3, 0, 7, 0, 0, 4, 0],
        [0, 7, 8, 0, 0, 1, 0, 0, 0],
        [9, 0, 0, 0, 5, 0, 0, 0, 0],
        [0, 4, 0, 6, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 7, 0, 0, 2],
        [5, 0, 0, 0, 4, 0, 7, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 0, 6]]


solveSudoku(grid)

# def check(grid, row, col):
#     for x in range(9):
#         if x != col and grid[row][x] == grid[row][col]: return False
#
#     for y in range(9):
#         if y != row and grid[y][col] == grid[row][col]: return False
#
#     for x in range(3):
#         for y in range(3):
#             x += col%3
#             y += row%3
#             if x != col and y != row and grid[x][y] == grid[row][col]: return False
#
#     return True


'''
def check(grid, row, col):
    for i in range(9):
        if (i!=row and grid[i][col] == grid[row][col]) or (i!= col and grid[row][i] == grid[row][col]) : return False

        r = (row//3)*3
        c = (col//3)*3
        for i in range(3):
            for j in range(3):
                if grid [r+i][c+j] == grid[i][j]: return False

        return True

def solve(grid, row=0, col=0, num=1):
    if (row==8 and col == 9): return True

    if (col>=9):
        row+=1
        col=0

    if grid[row][col] > 0:
        return solve(grid, row, col+1, 1)

    for i in range(1,10):
        if check(grid, row, col):
            grid[row][col] = i
            if solve(grid, row, col+1, 1): return True
        grid[row][col] = 0

    return False


def solveSudoku(grid):

    if solve(grid):
        for i in range(9):
            for j in range(9):
                print (grid[i][j])
            print('||')
    else:
        print ('NOT A VALID SUDOKU')

grid = [[0, 0, 0, 0, 9, 0, 0, 2, 0],
        [4, 0, 2, 5, 0, 0, 0, 6, 0],
        [0, 5, 3, 0, 7, 0, 0, 4, 0],
        [0, 7, 8, 0, 0, 1, 0, 0, 0],
        [9, 0, 0, 0, 5, 0, 0, 0, 0],
        [0, 4, 0, 6, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 7, 0, 0, 2],
        [5, 0, 0, 0, 4, 0, 7, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 0, 6]]
solveSudoku(grid)
'''
