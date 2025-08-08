#     Title : Tic Tac Toe
#     Engine : python
#     Author : Mansi Patel
#     Date : 2025-02-27

import tkinter as tk
from tkinter import messagebox
import numpy as np
import random


class TicTacToeGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Tic Tac Toe")
        self.game = TicTacToe()
        self.current_player = "X"
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.mode = None
        self.ai_player = None  # AI player object
        self.create_menu()

    def create_menu(self):
        menu_frame = tk.Frame(self.root)
        menu_frame.pack(pady=20)

        tk.Label(menu_frame, text="Choose Game Mode:", font=("Helvetica", 14)).pack(pady=5)

        tk.Button(
            menu_frame, text="Player vs Player",fg=("white"),bg=("Red"), font=("Helvetica", 12), command=self.start_pvp
        ).pack(pady=5)

        tk.Button(
            menu_frame, text="Player vs AI",fg=("white"),bg=("Red"), font=("Helvetica", 12), command=self.select_ai_level
        ).pack(pady=5)

    def start_pvp(self):
        self.mode = "PVP"
        self.setup_game()

    def select_ai_level(self):
        ai_level_frame = tk.Frame(self.root)
        ai_level_frame.pack(pady=20)

        tk.Label(ai_level_frame, text="Select AI Difficulty:", font=("Helvetica", 14)).pack(pady=5)

        tk.Button(
            ai_level_frame,
            text="Easy",
            font=("Helvetica", 12),
            command=lambda: self.start_pvai("Easy"),
        ).pack(pady=5)

        tk.Button(
            ai_level_frame,
            text="Medium",
            font=("Helvetica", 12),
            command=lambda: self.start_pvai("Medium"),
        ).pack(pady=5)

        tk.Button(
            ai_level_frame,
            text="Hard",
            font=("Helvetica", 12),
            command=lambda: self.start_pvai("Hard"),
        ).pack(pady=5)

    def start_pvai(self, difficulty):
        self.mode = "PVA"
        if difficulty == "Easy":
            self.ai_player = RandomAIPlayer("O")
        elif difficulty == "Medium":
            self.ai_player = MediumAIPlayer("O")
        elif difficulty == "Hard":
            self.ai_player = HardAIPlayer("O")
        self.setup_game()

    def setup_game(self):
        # Clear the root window and set up the game
        for widget in self.root.winfo_children():
            widget.destroy()

        self.create_widgets()

    def create_widgets(self):
        frame = tk.Frame(self.root)
        frame.pack()

        for i in range(3):
            for j in range(3):
                button = tk.Button(
                    frame,
                    text="",
                    font=("Helvetica", 24),
                    height=2,
                    width=5,
                    command=lambda row=i, col=j: self.on_click(row, col),
                )
                button.grid(row=i, column=j)
                self.buttons[i][j] = button

        self.reset_button = tk.Button(
            self.root, text="Reset Game", font=("Helvetica", 14), command=self.reset_game
        )
        self.reset_button.pack(pady=10)

    def on_click(self, row, col):
        square = row * 3 + col
        if self.game.board[row, col] == " " and not self.game.current_winner:
            self.game.make_move(square, self.current_player)
            self.update_gui()

            if self.game.current_winner:
                messagebox.showinfo("Game Over", f"{self.current_player} wins!")
                self.disable_buttons()
                self.ask_play_again()
            elif not self.game.empty_squares():
                messagebox.showinfo("Game Over", "It's a tie!")
                self.ask_play_again()
            else:
                if self.mode == "PVA" and self.current_player == "X":
                    self.current_player = "O"
                    self.ai_move()
                else:
                    self.current_player = "O" if self.current_player == "X" else "X"

    def ai_move(self):
        square = self.ai_player.get_move(self.game)
        row, col = divmod(square, 3)
        self.on_click(row, col)

    def update_gui(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text=self.game.board[i, j])

    def disable_buttons(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(state=tk.DISABLED)

    def reset_game(self):
        self.game.reset_game()
        self.current_player = "X"
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text="", state=tk.NORMAL)

    def ask_play_again(self):
        if messagebox.askyesno("Play Again", "Do you want to play again?"):
            self.reset_game()
        else:
            self.root.quit()

    def start(self):
        self.root.mainloop()


class TicTacToe:
    def __init__(self):
        self.board = np.full((3, 3), " ")
        self.current_winner = None

    def make_move(self, square, letter):
        row, col = divmod(square, 3)
        if self.board[row, col] == " ":
            self.board[row, col] = letter
            if self.check_winner(row, col, letter):
                self.current_winner = letter
            return True
        return False

    def check_winner(self, row, col, letter):
        if all(self.board[row, :] == letter):
            return True
        if all(self.board[:, col] == letter):
            return True
        if row == col and all(np.diag(self.board) == letter):
            return True
        if row + col == 2 and all(np.diag(np.fliplr(self.board)) == letter):
            return True
        return False

    def empty_squares(self):
        return " " in self.board

    def available_moves(self):
        return [i * 3 + j for i in range(3) for j in range(3) if self.board[i, j] == " "]

    def reset_game(self):
        self.__init__()


class RandomAIPlayer:
    def __init__(self, letter):
        self.letter = letter

    def get_move(self, game):
        return random.choice(game.available_moves())


class MediumAIPlayer:
    def __init__(self, letter):
        self.letter = letter

    def get_move(self, game):
        for letter in [self.letter, "X" if self.letter == "O" else "O"]:
            for move in game.available_moves():
                game_copy = TicTacToe()
                game_copy.board = np.copy(game.board)
                game_copy.make_move(move, letter)
                if game_copy.current_winner == letter:
                    return move
        return RandomAIPlayer(self.letter).get_move(game)


class HardAIPlayer:
    def __init__(self, letter):
        self.letter = letter

    def get_move(self, game):
        if len(game.available_moves()) == 9:
            return random.choice(game.available_moves())
        else:
            return self.minimax(game, self.letter)["position"]

    def minimax(self, state, player):
        max_player = self.letter
        other_player = "O" if player == "X" else "X"

        if state.current_winner == other_player:
            return {"position": None, "score": 1 * (len(state.available_moves()) + 1) if other_player == max_player else -1 * (len(state.available_moves()) + 1)}
        elif not state.empty_squares():
            return {"position": None, "score": 0}

        if player == max_player:
            best = {"position": None, "score": -float("inf")}
        else:
            best = {"position": None, "score": float("inf")}

        for possible_move in state.available_moves():
            state.make_move(possible_move, player)
            sim_score = self.minimax(state, other_player)
            state.board[possible_move // 3, possible_move % 3] = " "
            state.current_winner = None
            sim_score["position"] = possible_move

            if player == max_player:
                if sim_score["score"] > best["score"]:
                    best = sim_score
            else:
                if sim_score["score"] < best["score"]:
                    best = sim_score

        return best


if __name__ == "__main__":
    app = TicTacToeGUI()
    app.start()