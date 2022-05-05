import math
from tkinter import *

import numpy as np

human, computer, tie = 'O', 'X', 'T'
board = [['_', '_', '_'], ['_', '_', '_'], ['_', '_', '_']]
size_of_board = 800
size_of_grid = 600
grid_square_size = size_of_grid // 3
margin = 50
symbol_X_color = '#FF0000'
symbol_O_color = '#000000'
canvas: Canvas
who_is_starting = computer
who_is_playing = human
window: Tk
isGameOver = False
who_won = ''
use_alpha_beta_pruning = True
count = 0
alpha_count = 0


# to check if game is over and result is tie
def is_there_any_square_left_empty_on_board():
    return "_" in np.array(board)


# to check if the place is available to be played on
def is_square_occupied(grid_position):
    if board[grid_position[0]][grid_position[1]] != '_':
        return True
    return False


# check all possible winning scenarios
def is_there_any_winner(player):
    if (
            (board[0].count(player) == 3) or
            (board[1].count(player) == 3) or
            (board[2].count(player) == 3) or
            (board[0][0] == player and board[1][0] == player and board[2][0] == player) or
            (board[0][1] == player and board[1][1] == player and board[2][1] == player) or
            (board[0][2] == player and board[1][2] == player and board[2][2] == player) or
            (board[0][0] == player and board[1][1] == player and board[2][2] == player) or
            (board[0][2] == player and board[1][1] == player and board[2][0] == player)
    ):
        return True
    else:
        return False


# This function is for AI. Calls Minimax as recursive to play the best move it can
def find_best_move():
    global who_is_playing, count, alpha_count
    count = 0
    alpha_count = 0
    who_is_playing = computer
    best_score = -math.inf
    best_move = [-1, -1]
    for i in range(3):
        for j in range(3):
            if not is_square_occupied([i, j]):
                board[i][j] = "X"
                score = minimax(0, False, -math.inf, math.inf)
                board[i][j] = "_"
                if score > best_score:
                    best_score = score
                    best_move = [i, j]
    board[best_move[0]][best_move[1]] = 'X'
    print(count, alpha_count)
    draw_X(best_move)
    who_is_playing = human


# Minimax algorithm. Find best move for the AI until there is no possible situations left
def minimax(depth, is_max, alpha, beta):
    global count, alpha_count
    count += 1
    if is_there_any_winner(human):
        return -1
    elif is_there_any_winner(computer):
        return 1
    elif not is_there_any_square_left_empty_on_board():
        return 0

    if is_max:
        best_score = -math.inf
        for i in range(3):
            for j in range(3):
                if not is_square_occupied([i, j]):
                    board[i][j] = 'X'
                    best_score = max(best_score, minimax(depth + 1, False, alpha, beta))
                    alpha = max(alpha, best_score)
                    board[i][j] = '_'
                    if use_alpha_beta_pruning and beta <= alpha:
                        alpha_count += 1
                        break

        return best_score
    else:
        best_score = math.inf
        for i in range(3):
            for j in range(3):
                if not is_square_occupied([i, j]):
                    board[i][j] = 'O'
                    best_score = min(best_score, minimax(depth + 1, True, alpha, beta))
                    beta = min(beta, best_score)
                    board[i][j] = '_'
                    if use_alpha_beta_pruning and beta <= alpha:
                        alpha_count += 1
                        break

        return best_score


# Human player starts the game first
def start_game_human_first():
    global who_is_starting
    who_is_starting = human
    create_game_board_ui()


# AI starts the game first
def start_game_ai_first():
    global who_is_starting
    who_is_starting = computer
    create_game_board_ui()


# Draw grid canvas for the Tic-Tac-Toe
def create_game_board_ui():
    global canvas
    global window
    canvas = Canvas(window, width=size_of_grid, height=size_of_grid, bd=0, highlightthickness=0)
    canvas.place(relx=0.5, rely=0.5, anchor=CENTER)
    canvas.bind('<Button-1>', click)
    initialize_board()
    if who_is_starting == human:
        window.mainloop()
    else:
        window.after(10, find_best_move())
        window.mainloop()


# Check whether the game is over or not
def check_game_status():
    global who_won
    global isGameOver
    isGameOver = False
    if is_there_any_winner(human):
        who_won = human
        isGameOver = True
    elif is_there_any_winner(computer):
        who_won = computer
        isGameOver = True
    elif not is_there_any_square_left_empty_on_board():
        who_won = tie
        isGameOver = True

    if isGameOver:
        show_game_over()
    return isGameOver


# UI for the welcome page to start game. Human player first or AI first
def create_welcome_page():
    global canvas
    reset_globals()
    canvas = Canvas(window, width=size_of_grid, height=size_of_grid, bd=0, highlightthickness=0)
    canvas.place(relx=0.5, rely=0.5, anchor=CENTER)
    canvas.create_text(300, 50, text="        Tic-Tac-Toe \n\t by \n    Yasar Can Kakdas", fill="black",
                       font='TimesNewRoman 20 bold')
    human_first_button = Button(text="Player starts first", command=start_game_human_first,
                                font='TimesNewRoman 14 bold')
    human_first_button.place(width=200, height=80, x=200, y=250)
    ai_first_button = Button(text="AI starts first", command=start_game_ai_first, font='TimesNewRoman 14 bold')
    ai_first_button.place(width=200, height=80, x=420, y=250)
    window.mainloop()


# Reset global variables to restart the game
def reset_globals():
    global isGameOver, who_won, board, who_is_playing
    isGameOver = False
    who_is_playing = human
    who_won = ''
    board = [['_', '_', '_'], ['_', '_', '_'], ['_', '_', '_']]


# Popup UI for showing the results of the game
def show_game_over():
    top = Toplevel(window)
    top.geometry("500x500")
    top.title("Game Over")
    Label(top, text="GAME OVER!", font='Mistral 50 bold').place(x=100, y=80)

    if who_won == human:
        Label(top, text="YOU WON!", font='Mistral 50 bold', fg="#f00").place(x=100, y=180)
    elif who_won == computer:
        Label(top, text="AI WON :)", font='Mistral 50 bold', fg="#f00").place(x=130, y=180)
    else:
        Label(top, text="It's a Tie!", font='Mistral 50 bold', fg="#f00").place(x=130, y=180)
    top.grab_set()

    restart_button = Button(master=top, text="RESTART", command=lambda: {
        top.destroy(),
        create_welcome_page()
    }, font='TimesNewRoman 14 bold')
    restart_button.place(width=100, height=50, x=120, y=300)
    exit_button = Button(master=top, text="EXIT", command=window.destroy, font='TimesNewRoman 14 bold')
    exit_button.place(width=100, height=50, x=250, y=300)
    top.mainloop()


# Draw grid
def initialize_board():
    for i in range(4):
        if i == 0:
            canvas.create_line(0, 0, size_of_grid - 1, 0)
        else:
            canvas.create_line(0, i * grid_square_size - 1, size_of_grid - 1,
                               i * grid_square_size - 1)
    for i in range(4):
        if i == 0:
            canvas.create_line(0, 0, 0, size_of_grid - 1)
        else:
            canvas.create_line(i * grid_square_size - 1, 0, i * grid_square_size - 1,
                               size_of_grid - 1)
    for i in range(3):
        for j in range(3):
            if board[i][j] == 'X':
                draw_X([i, j])
            elif board[i][j] == 'O':
                draw_O([i, j])


# Draw "O" when player clicks an empty space
def draw_O(grid_position):
    global isGameOver
    board[grid_position[0]][grid_position[1]] = 'O'
    start_pos = [grid_position[1] * grid_square_size + margin, grid_position[0] * grid_square_size + margin]
    end_pos = [(grid_position[1] + 1) * grid_square_size - margin,
               (grid_position[0] + 1) * grid_square_size - margin]
    canvas.create_oval(start_pos[0], start_pos[1], end_pos[0], end_pos[1], width=20, outline=symbol_O_color)
    isGameOver = check_game_status()
    if not isGameOver:
        find_best_move()


# Draw "X" for the AI's turn
def draw_X(grid_position):
    global isGameOver
    board[grid_position[0]][grid_position[1]] = 'X'
    line1_start_pos = [grid_position[1] * grid_square_size + margin, grid_position[0] * grid_square_size + margin]
    line1_end_pos = [(grid_position[1] + 1) * grid_square_size - margin,
                     (grid_position[0] + 1) * grid_square_size - margin]

    line2_start_pos = [line1_start_pos[0] + grid_square_size - 2 * margin, line1_start_pos[1]]
    line2_end_pos = [line1_end_pos[0] - grid_square_size + 2 * margin, line1_end_pos[1]]

    canvas.create_line(line1_start_pos[0], line1_start_pos[1], line1_end_pos[0], line1_end_pos[1], width=20,
                       fill=symbol_X_color)
    canvas.create_line(line2_start_pos[0], line2_start_pos[1], line2_end_pos[0], line2_end_pos[1], width=20,
                       fill=symbol_X_color)
    isGameOver = check_game_status()


def click(event):
    if (who_is_playing is computer) or isGameOver:
        return

    grid_position = [event.y // grid_square_size, event.x // grid_square_size]
    if not is_square_occupied(grid_position):
        draw_O(grid_position)


if __name__ == '__main__':
    window = Tk()
    window.resizable(False, False)
    window.title('Tic-Tac-Toe')
    window.geometry(f'{size_of_board}x{size_of_board}')
    create_welcome_page()
