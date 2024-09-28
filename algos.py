# Algorithms for traversing the game board

from collections import deque as queue

board = [[1, 2, 3, 4, 5],
         [6, 7, 8, 9, 10],
         [11, 12, 13, 14, 15],
         [16, 17, 18, 19, 20],
         [21, 22, 23, 24, 25]]

ROW = 5
COL = 5

# Direction Vectors
# negative column is considered going up
X = [0, 1, 1, 1, 0, -1, -1, -1] # row
Y = [-1, -1, 0, 1, 1, 1, 0, -1] # column 
vis = [[False for i in range(5)] for j in range(5)] # visited squares


def isValid(visited, row, col):
    global ROW 
    global COL
    global vis

    # if cell's out of bounds
    if (row < 0 or col < 0 or row >= ROW or col >= COL):
        # TODO STOPPED  https://www.geeksforgeeks.org/depth-first-traversal-dfs-on-a-2d-array/
        return False
    
    # if cell is already visited
    if (vis[row][col]):
        return False
    
    # else visit
    return True

# depth-first algorithm to search board for valid words
# uses matrix grid[]
def DFS(row, col, grid): # grid = board
    global X 
    global Y
    global vis

    # initialize a stack of pairs, push starting cell
    st = []
    st.append([row, col])

    # iterate until stack not empty
    while (len(st) > 0):
        # pop top pair
        curr = st[len(st) -1]
        st.remove(st[len(st) - 1])
        row = curr[0]
        col = curr[1]

        # check if current popped cell
        # is valid
        if (isValid(row, col) == False):
            continue

        # mark current cell as visited
        vis[row][col] = True 

        # print element at current top cell
        print(grid[row][col], end = " ")

        # push all adjacent cells
        # from direction vectors
        for i in range(8):
            adjx = row + X[i]
            adjy = col + Y[i]
            st.append([adjx, adjy])

def BFS(grid, vis, row, col):
    # stores indices of matrix cells
    q = queue()

    # mark starting cell visited and push to queue
    q.append((row, col))
    vis[row][col] = True

    # iterate while queue not empty
    while (len(q) > 0):
        cell = q.popleft()
        x = cell[0]
        y = cell[1]
        print(grid[x][y], end = " ")

        # go to adjacent cells
        for i in range(8):
            adjx = x + X[i]
            adjy = y + Y[i]
            if (isValid(vis, adjx, adjy)):
                q.append((adjx, adjy))
                vis[adjx][adjy] = True


def wordSearch(grid, vis, row, col):
    # stores indices of matrix cells
    q = queue()

    # mark starting cell visited and push to queue
    q.append((row, col))
    vis[row][col] = True

    # iterate while queue not empty
    while (len(q) > 0):
        cell = q.popleft()
        x = cell[0]
        y = cell[1]
        print(grid[x][y], end = " ")

     # go to adjacent cells
        for i in range(8):
            adjx = x + X[i]
            adjy = y + Y[i]
            if (isValid(vis, adjx, adjy)):
                q.append((adjx, adjy))
                vis[adjx][adjy] = True

# BFS on 2d Array
# https://www.geeksforgeeks.org/depth-first-traversal-dfs-on-a-2d-array/


#DFS(0,0, board)
BFS(board, vis, 0, 0)