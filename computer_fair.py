import tkinter as tk

# I. Imports & Constants
ROWS = 6
COLS = 7
SQUARE_SIZE = 100
RADIUS = SQUARE_SIZE // 2 - 5
BG_COLOR = "blue"
EMPTY_COLOR = "white"
PLAYER_COLORS = ["red", "yellow"]

# II. Game Logic Class (Connect4Game)
class Connect4Game:
    def __init__(self):
        # Initialize board as 2D list and set starting player
        self.board = [[None for _ in range(COLS)] for _ in range(ROWS)]
        self.current_player = 0

    def is_valid_move(self, col):
        # A move is valid if the top cell in the column is empty
        return self.board[0][col] is None

    def drop_piece(self, col):
        if not self.is_valid_move(col):
            return None
        # Place piece in the lowest available row in the column
        for row in range(ROWS - 1, -1, -1):
            if self.board[row][col] is None:
                self.board[row][col] = self.current_player
                return row, col
        return None

    def check_win(self, row, col):
        # Check if placing a piece at (row, col) wins the game
        player = self.board[row][col]
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for dr, dc in directions:
            count = 1
            # Check in the positive direction
            r, c = row + dr, col + dc
            while 0 <= r < ROWS and 0 <= c < COLS and self.board[r][c] == player:
                count += 1
                r += dr
                c += dc
            # Check in the negative direction
            r, c = row - dr, col - dc
            while 0 <= r < ROWS and 0 <= c < COLS and self.board[r][c] == player:
                count += 1
                r -= dr
                c -= dc
            if count >= 4:
                return True
        return False

    def switch_player(self):
        self.current_player = 1 - self.current_player

# III. GUI Class (Connect4GUI)
class Connect4GUI:
    def __init__(self, game):
        self.game = game
        self.game_over = False
        self.window = tk.Tk()
        self.window.title("Connect 4")
        self.canvas = tk.Canvas(self.window, width=COLS * SQUARE_SIZE, height=ROWS * SQUARE_SIZE, bg=BG_COLOR)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.handle_click)
        self.draw_board()

    def draw_board(self):
        self.canvas.delete("all")
        for r in range(ROWS):
            for c in range(COLS):
                x1 = c * SQUARE_SIZE + 5
                y1 = r * SQUARE_SIZE + 5
                x2 = (c + 1) * SQUARE_SIZE - 5
                y2 = (r + 1) * SQUARE_SIZE - 5
                piece = self.game.board[r][c]
                color = EMPTY_COLOR if piece is None else PLAYER_COLORS[piece]
                self.canvas.create_oval(x1, y1, x2, y2, fill=color)

    def handle_click(self, event):
        if self.game_over:
            return
        col = event.x // SQUARE_SIZE
        if col < 0 or col >= COLS:
            return
        move = self.game.drop_piece(col)
        if move:
            row, col = move
            self.draw_board()
            if self.game.check_win(row, col):
                self.game_over = True
                self.canvas.create_text(
                    COLS * SQUARE_SIZE // 2, ROWS * SQUARE_SIZE // 2,
                    text=f"Player {self.game.current_player + 1} wins!",
                    font="Arial 24 bold", fill="black"
                )
            else:
                self.game.switch_player()

# IV. Main Execution
def main():
    game = Connect4Game()
    gui = Connect4GUI(game)
    tk.mainloop()

if __name__ == "__main__":
    main()

