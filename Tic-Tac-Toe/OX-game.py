#     Title : Tic Tac Toe
#     Engine : python
#     Author : Mansi Patel
#     Date : 2025-02-27

import random
import numpy as np
import qrcode

class QRCodeGenerator:

    def generate_qr(self):
        qr= qrcode.QRCode(version=1, box_size=10, border=5, error_correction=qrcode.constants.ERROR_CORRECT_H)
        data="https://playtictactoe.org/"
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="pink", back_color="white")
        return img.show()

class TicTacToe:
    def __init__(self, size=3):
        self.size = size
        self.board = np.full((size, size), " ")
        self.current_winner = None

    def print_board(self):
        for row in self.board:
            print("| " + " | ".join(row) + " |")

    def print_board_indices(self):
        indices = np.arange(self.size * self.size).reshape(self.size, self.size)
        for row in indices:
            print("| " + " | ".join(map(str, row)) + " |")

    def wrap_index(self, index):
        return index % (self.size * self.size)

    def make_move(self, square, letter):
        square = self.wrap_index(square)
        row, col = divmod(square, self.size)
        if self.board[row, col] == " ":
            self.board[row, col] = letter
            if self.check_winner(row, col, letter):
                self.current_winner = letter
            return True
        return False

    def check_winner(self, row, col, letter):
        win_condition = self.size if self.size == 3 else 4
        
        if all(self.board[row, i] == letter for i in range(self.size)):
            return True
        
        if all(self.board[i, col] == letter for i in range(self.size)):
            return True
        
        if row == col and all(self.board[i, i] == letter for i in range(self.size)):
            return True
        
        if row + col == self.size - 1 and all(self.board[i, self.size - 1 - i] == letter for i in range(self.size)):
            return True
        
        return False

    def empty_squares(self):
        return " " in self.board

    def available_moves(self):
        return [i * self.size + j for i in range(self.size) for j in range(self.size) if self.board[i, j] == " "]

    def reset_game(self):
        self.__init__(self.size)

class Player:
    def __init__(self, letter):
        self.letter = letter

class HumanPlayer(Player):
    def get_move(self, game):
        valid_square = False
        val = None
        while not valid_square:
            square = input(f"{self.letter}'s turn. Input move (0-{game.size*game.size - 1}): ")
            try:
                val = int(square)
                val = game.wrap_index(val)
                if val not in game.available_moves():
                    raise ValueError
                valid_square = True
            except ValueError:
                print("Invalid move. Try again.")
        return val

class RandomAIPlayer(Player):
    def __init__(self, letter, difficulty=1):
        super().__init__(letter)
        self.difficulty = difficulty

    def get_move(self, game):
        if self.difficulty == 1:
            square = random.choice(game.available_moves())
        elif self.difficulty == 2:
            square = self.medium_move(game)
        else:
            square = self.hard_move(game)
        print(f"{self.letter} (AI) chooses square {square}")
        return square

    def medium_move(self, game):
        # Implement medium difficulty logic
        return random.choice(game.available_moves())

    def hard_move(self, game):
        # Implement hard difficulty logic
        return random.choice(game.available_moves())

class MinimaxAIPlayer(Player):
    def __init__(self, letter, depth=None, difficulty=3):
        super().__init__(letter)
        self.depth = depth
        self.difficulty = difficulty

    def get_move(self, game):
        if self.difficulty == 1:
            square = random.choice(game.available_moves())
        elif self.difficulty == 2:
            square = self.minimax(game, self.letter, 1)['position']
        else:
            square = self.minimax(game, self.letter, self.depth)['position']
        print(f"{self.letter} (AI) chooses square {square}")
        return square

    def minimax(self, state, player, depth):
        if depth == 0:
            return {'position': None, 'score': 0}

        max_player = self.letter
        other_player = 'O' if player == 'X' else 'X'

        if state.current_winner == other_player:
            return {'position': None, 'score': 1 * (state.size * state.size + 1) if other_player == max_player else -1 * (state.size * state.size + 1)}

        elif not state.empty_squares():
            return {'position': None, 'score': 0}

        if player == max_player:
            best = {'position': None, 'score': -float('inf')}
        else:
            best = {'position': None, 'score': float('inf')}

        for possible_move in state.available_moves():
            row, col = divmod(possible_move, state.size)
            state.board[row, col] = player
            if state.check_winner(row, col, player):
                state.current_winner = player

            sim_score = self.minimax(state, other_player, depth - 1)

            state.board[row, col] = ' '
            state.current_winner = None
            sim_score['position'] = possible_move

            if player == max_player:
                if sim_score['score'] > best['score']:
                    best = sim_score
            else:
                if sim_score['score'] < best['score']:
                    best = sim_score

        return best

class Game:
    def __init__(self, x_player, o_player, size=3, print_game=True):
        self.tic_tac_toe = TicTacToe(size)
        self.x_player = x_player
        self.o_player = o_player
        self.print_game = print_game
        self.funny_messages = [
            "Plotting world domination, one X at a time...",
            "O my! What a move!",
            "That move was smoother than butter on a bald monkey!",
            "Are you sure you're not a Tic Tac Pro?",
            "Warning: Excessive gaming may cause extreme awesomeness!",
            "Plot twist: The O's were X's in disguise all along!",
            "Breaking news: Local player makes incredible move!",
            "That move was so good, even the AI is sweating!",
            "Loading next move... Please wait... Just kidding!",
            "Is this chess? No? My bad, carry on!"
        ]

    def get_random_message(self):
        return random.choice(self.funny_messages)

    def play(self):
        if self.print_game:
            print("\nBoard positions:")
            self.tic_tac_toe.print_board_indices()

        letter = "X"
        moves_count = 0
        while self.tic_tac_toe.empty_squares():
            # Show a funny message every 2 moves
            if moves_count % 2 == 0:
                print("\n" + self.get_random_message() + "\n")
            
            if letter == "O":
                square = self.o_player.get_move(self.tic_tac_toe)
            else:
                square = self.x_player.get_move(self.tic_tac_toe)

            if self.tic_tac_toe.make_move(square, letter):
                if self.print_game:
                    print(f"\n{letter} makes a move to square {square}")
                    self.tic_tac_toe.print_board()
                    print("")

                if self.tic_tac_toe.current_winner:
                    win_messages = [
                        f"Holy smokes! {letter} just won like a boss! 🎉",
                        f"Ladies and gentlemen, we have a winner! It's {letter}! 🏆",
                        f"{letter} wins! Time to do a victory dance! 💃",
                        f"Game over! {letter} is taking home the virtual trophy! 🎮"
                    ]
                    print(random.choice(win_messages))
                    return letter
                letter = "O" if letter == "X" else "X"

        tie_messages = [
            "It's a tie! Just like my shoelaces!",
            "Well, well, well... looks like we're all winners here! (Or losers, depending on your perspective 😉)",
            "Tie game! Time to settle this with a dance-off!",
            "Draw! Like a cowboy showdown, but with X's and O's!"
            "It's a tie! No winners, no losers, just a whole lot of fun!"
        ]
        print(random.choice(tie_messages))
        return "Tie"

class GameSetup:
    def choose_board_size(self):
        while True:
            print("Choose board size:")
            print("1. 3x3")
            print("2. 5x5")
            size_choice = input("Enter your choice (1 or 2): ")
            if size_choice in ["1", "2"]:
                return 3 if size_choice == "1" else 5
            print("Invalid choice. Please try again.")

    def choose_game_mode(self):
        while True:
            print("Choose game mode:")
            print("1. Player1 vs Player2")
            print("2. Player vs Random AI")
            print("3. Player vs Minimax AI")
            mode = input("Enter your choice (1, 2, or 3): ")
            if mode == "1":
                return HumanPlayer("X"), HumanPlayer("O")
            elif mode == "2":
                difficulty = self.choose_ai_difficulty()
                return HumanPlayer("X"), RandomAIPlayer("O", difficulty)
            elif mode == "3":
                difficulty = self.choose_ai_difficulty()
                depth = {1: 1, 2: 3, 3: None}[difficulty]
                return HumanPlayer("X"), MinimaxAIPlayer("O", depth, difficulty)
            print("Invalid choice. Please try again.")

    def choose_ai_difficulty(self):
        while True:
            print("Choose AI difficulty level:")
            print("1. Easy")
            print("2. Medium")
            print("3. Hard")
            difficulty = input("Enter your choice (1, 2, or 3): ")
            if difficulty in ["1", "2", "3"]:
                return int(difficulty)
            print("Invalid choice. Please try again.")

class MainGame:
    def __init__(self):
        self.qr_generator = QRCodeGenerator()
        self.game_setup = GameSetup()

    def start(self):
        tips = input("Do you want to play online Tic Tac Toe? (y/n): ").lower()
        if tips == "y":
            self.qr_generator.generate_qr()
            print("Scan the QR code to play online!")
            input("Press Enter after scanning the QR code to start the game...")

        print("Welcome to Tic Tac Toe!")

        while True:
            size = self.game_setup.choose_board_size()
            x_player, o_player = self.game_setup.choose_game_mode()

            game = Game(x_player, o_player, size)
            game.play()

            replay = input("Do you want to play again? (y/n): ").lower()
            if replay != "y":
                print("Thanks for playing! Goodbye.")
                break

def main():
    main_game = MainGame()
    main_game.start()

if __name__ == "__main__":
    main()
