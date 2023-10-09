class Player:
    def __init__(self, symbol, x, y, walls):
        self.symbol = symbol
        self.x = x
        self.y = y
        self.walls = walls

class Board:
    def __init__(self):
        self.size = 9
        self.board = [['.' for _ in range(self.size)] for _ in range(self.size)]

    def is_proper_input(self, x, y):
        return 0 <= x < self.size and 0 <= y < self.size and self.board[x][y] == "."

    def is_legal_move(self, player, x, y):
        if not self.is_proper_input(x, y):
            return False

        dx = x - player.x
        dy = y - player.y

        return (dx == 1 and dy == 0) or (dx == -1 and dy == 0) or (dx == 0 and dy == 1) or (dx == 0 and dy == -1)

    def can_place_wall(self, player, x1, y1, x2, y2):
        if self.is_proper_input(x1, y1) and self.is_proper_input(x2, y2):
            # Place the wall and check if there's a path for the player
            self.board[x1][y1] = "#"
            self.board[x2][y2] = "#"
            player_can_reach = self.is_legal_move(player, player.x, player.y)

            # Return board to its state before placing the wall
            self.board[x1][y1] = "."
            self.board[x2][y2] = "."

            return not player_can_reach

        return False

    def place_wall(self, player, x1, y1, x2, y2):
        if self.can_place_wall(player, x1, y1, x2, y2):
            self.board[x1][y1] = "#"
            self.board[x2][y2] = "#"
            player.walls -= 1
            return True

        return False

    def place_player(self, player):
        self.board[player.x][player.y] = player.symbol

    def move(self, player, direction):
        x, y = player.x, player.y
        if direction == 'U':
            x -= 1
        elif direction == 'D':
            x += 1
        elif direction == 'L':
            y -= 1
        elif direction == 'R':
            y += 1

        if self.is_legal_move(player, x, y):
            self.board[player.x][player.y] = "."
            player.x = x
            player.y = y
            self.board[x][y] = player.symbol
            return True

        return False

    def is_game_over(self, player):
        return (player.symbol == 'X' and player.x == 8) or (player.symbol == 'O' and player.x == 0)

    def draw(self, players):
        print("   " + " ".join(str(i) for i in range(0, 9)))  # Print column numbers
        for i, row in enumerate(self.board):
            print(f"{i:2} {' '.join(row)}")  # Print row number and board content
        print(f"Player X : {players[0].walls} walls remaining")
        print(f"Player O : {players[1].walls} walls remaining")

def main():
    player1 = Player('X', 0, 4, 10)
    player2 = Player('O', 8, 4, 10)
    board = Board()
    board.place_player(player1)
    board.place_player(player2)

    players = [player1, player2]
    currentPlayer = 0

    while True:
        board.draw(players)
        print(f"Player {players[currentPlayer].symbol}'s turn")
        move_type = input("M for Move, W for Wall: ").upper()

        if move_type == 'M':
            direction = input("Enter U (Up), D (Down), L (Left), R (Right): ").upper()
            if direction in ['U', 'D', 'L', 'R']:
                if board.move(players[currentPlayer], direction):
                    if board.is_game_over(players[currentPlayer]):
                        board.draw(players)
                        print(f"Player {players[currentPlayer].symbol} wins!")
                        break
                    currentPlayer = 1 - currentPlayer
                else:
                    print("Invalid move")
            else:
                print("Invalid direction")

        elif move_type == 'W':
            x1, y1, x2, y2 = map(int, input("Two coordinates (e.g., '4 5 4 4'): ").split())
            if players[currentPlayer].walls > 0 and board.place_wall(players[currentPlayer], x1, y1, x2, y2):
                currentPlayer = 1 - currentPlayer
            else:
                print("Invalid wall placement. Try again.")
        else:
            print("Invalid input. Enter 'M' or 'W'.")


if __name__ == "__main__":
    main()
