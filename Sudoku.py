import time

start = time.perf_counter()

def board_draft_start(board, board_draft):
    for i in range(9):
        for j in range(9):
            if board[i][j] != 0:
                board_draft[i][j] = board[i][j]

def find_square(line, col):
    return (line // 3) * 3 + col // 3

def get_square_draft(board_draft, square):
    square_draft = [
                [[], [], []],
                [[], [], []],
                [[], [], []],
            ]
    start_line = (square // 3) * 3
    start_col = (square % 3) * 3
    for line in range(start_line, start_line + 3):
        for col in range(start_col, start_col + 3):
            square_draft[line % 3][col % 3] = board_draft[line][col]
    return square_draft

def line(board, line, board_draft):
    for col in range(9):
        if board[line][col] == 0:
            start_line = (line // 3) * 3
            start_col = (col // 3) * 3
            for j in range(1, 10):
                flag = 0
                for k in range(9):
                    if board_draft[line][k] == j or board_draft[k][col] == j:
                        flag = 1
                        break
                if flag:
                    continue
                for m in range(start_line, start_line + 3):
                    for n in range(start_col, start_col + 3):
                        if board_draft[m][n] == j:
                            flag = 1
                            break
                    if flag:
                        break    
                if flag == 0:
                    board_draft[line][col].append(j)

def place_number(board, board_draft, line, col, num):
    board[line][col] = board_draft[line][col][num]
    board_draft[line][col] = board_draft[line][col][num]
    for i in range(9):
        if isinstance(board_draft[line][i], list) and board_draft[line][col] in board_draft[line][i]:
            board_draft[line][i].remove(board_draft[line][col])
        if isinstance(board_draft[i][col], list) and board_draft[line][col] in board_draft[i][col]:
            board_draft[i][col].remove(board_draft[line][col])
    start_line = (line // 3) * 3
    start_col = (col // 3) * 3
    for i in range(start_line, start_line + 3):
        for j in range(start_col, start_col + 3):
            if isinstance(board_draft[i][j], list) and board_draft[line][col] in board_draft[i][j]:
                board_draft[i][j].remove(board_draft[line][col])

def naked_single(board, board_draft, changes):
    for line in range(9):
        for col in range(9):
            if isinstance(board_draft[line][col], list):
                if len(board_draft[line][col]) == 1:
                    num = 0
                    place_number(board, board_draft, line, col, num)
                    changes += 1
    return changes

def hidden_single(board, board_draft, changes):
    for line in range(9):
        for i in range(1, 10):
            if i not in board_draft[line]:
                i_num = 0
                for col in range(9):
                    if isinstance(board_draft[line][col], list) and i in board_draft[line][col]:
                        i_num += 1
                        num = board_draft[line][col].index(i)
                        pos = [line, col, num]
                        if i_num > 1:
                            break
                if i_num == 1:
                    place_number(board, board_draft, pos[0], pos[1], pos[2])
                    changes += 1

    for col in range(9):
        for i in range(1, 10):
            i_in_col = 0
            for line in range(9):
                if board_draft[line][col] == i:
                    i_in_col += 1
            if i_in_col == 0:
                i_num = 0
                for line in range(9):
                    if isinstance(board_draft[line][col], list) and i in board_draft[line][col]:
                        i_num += 1
                        num = board_draft[line][col].index(i)
                        pos = [line, col, num]
                        if i_num > 1:
                            break
                if i_num == 1:
                    place_number(board, board_draft, pos[0], pos[1], pos[2])
                    changes += 1

    for square in range(9):
        square_draft = get_square_draft(board_draft, square)
        for i in range(1, 10):
            i_in_square = 0
            for j in range(3):
                if i in square_draft[j]:
                    i_in_square += 1
            if i_in_square == 0:
                i_num = 0
                for line in range(3):
                    for col in range(3):
                        if isinstance(square_draft[line][col], list) and i in square_draft[line][col]:
                            i_num += 1
                            num = square_draft[line][col].index(i)
                            pos = [(square // 3) * 3 + line, (square % 3) * 3 + col, num]
                if i_num == 1:
                    place_number(board, board_draft, pos[0], pos[1], pos[2])
                    square_draft = get_square_draft(board_draft, square)
                    changes += 1

    return changes

def show_result(board):
    for i in range(9):
        for j in range(9):
            if j == 2 or j == 5:
                print(board[i][j], end=' | ')
            else:
                print(board[i][j], end=' ')
        if i == 2 or i == 5:
            print()
            print('-' * 21)
        else:
            print()

board_draft = [
    [[], [], [], [], [], [], [], [], []],
    [[], [], [], [], [], [], [], [], []],
    [[], [], [], [], [], [], [], [], []],
    [[], [], [], [], [], [], [], [], []],
    [[], [], [], [], [], [], [], [], []],
    [[], [], [], [], [], [], [], [], []],
    [[], [], [], [], [], [], [], [], []],
    [[], [], [], [], [], [], [], [], []],
    [[], [], [], [], [], [], [], [], []],
]


board = [
    [0, 0, 0, 2, 0, 8, 4, 0, 0],
    [3, 9, 0, 0, 0, 0, 0, 1, 8],
    [0, 8, 4, 0, 9, 1, 7, 0, 0],
    [4, 0, 5, 8, 0, 0, 9, 0, 2],
    [0, 6, 0, 9, 2, 4, 0, 8, 0],
    [9, 0, 0, 0, 6, 0, 0, 0, 0],
    [0, 7, 0, 4, 0, 9, 5, 0, 0],
    [8, 0, 1, 0, 0, 2, 0, 0, 9],
    [0, 4, 9, 0, 1, 6, 8, 2, 0]
]

board_draft_start(board, board_draft)

for i in range(9):
    line(board, i, board_draft)

changes = 1
while changes != 0:
    changes = 0
    changes = naked_single(board, board_draft, changes)
    changes = hidden_single(board, board_draft, changes)

show_result(board)

end = time.perf_counter()
print(f"Execution time: {end - start:.6f} seconds")