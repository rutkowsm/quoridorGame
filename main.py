def draw(board, players):
    # Draw the board with walls, player positions, and index numbers
    print("   " + " ".join(str(i) for i in range(0, 9)))  # Print column numbers
    for i, row in enumerate(board):
        print(f"{i:2} {' '.join(row)}")  # Print row number and board content
    print(f"Player X : {players[0]['walls']} walls remaining")
    print(f"Player O : {players[1]['walls']} walls remaining")


def init(player1, player2):
    # Set up the board
    board = []
    for _ in range(9):
        row = ["."] * 9
        board.append(row)

    # Initial player positions
    board[player1['x']][player1['y']] = player1['symbol']
    board[player2['x']][player2['y']] = player2['symbol']

    return board


def is_proper_input(board, x, y):
    return 0 <= x < 9 and 0 <= y < 9 and board[x][y] == "."


def is_legal_move(board, player, x, y):
    if not is_proper_input(board, x, y):
        return False

    dx = x - player['x']
    dy = y - player['y']

    # Players can only move one square in any direction
    return (dx == 1 and dy == 0) or (dx == -1 and dy == 0) or (dx == 0 and dy == 1) or (dx == 0 and dy == -1)


def can_place_wall(board, player, x1, y1, x2, y2):
    if (is_proper_input(board, x1, y1) and is_proper_input(board, x2, y2)):
        # Place the wall and check if there's a path for the player
        board[x1][y1] = "#"
        board[x2][y2] = "#"
        player_can_reach = is_legal_move(board, player, player['x'], player['y'])

        # Return board to its state before placing the wall
        board[x1][y1] = "."
        board[x2][y2] = "."

        return not player_can_reach

    return False


def place_wall(board, player, x1, y1, x2, y2):
    if can_place_wall(board, player, x1, y1, x2, y2):
        board[x1][y1] = "#"
        board[x2][y2] = "#"
        player['walls'] -= 1
        return True

    return False


def move(board, player, direction):
    x, y = player['x'], player['y']
    if direction == 'U':
        x -= 1
    elif direction == 'D':
        x += 1
    elif direction == 'L':
        y -= 1
    elif direction == 'R':
        y += 1

    if is_legal_move(board, player, x, y):
        board[player['x']][player['y']] = "."
        player['x'] = x
        player['y'] = y
        board[x][y] = player['symbol']
        return True

    return False


def is_game_over(player):
    return (player['symbol'] == 'X' and player['x'] == 8) or (player['symbol'] == 'O' and player['x'] == 0)


def main():
    player1 = {'symbol': 'X', 'x': 0, 'y': 4, 'walls': 10}
    player2 = {'symbol': 'O', 'x': 8, 'y': 4, 'walls': 10}
    board = init(player1, player2)
    players = [player1, player2]
    currentPlayer = 0

    while True:
        draw(board, players)
        print("M - Move || W - Wall")
        inp = input(f"Player {players[currentPlayer]['symbol']}: ").upper()

        if inp == 'M':
            direction = input("Enter U (Up), D (Down), L (Left), R (Right): ").upper()
            if direction in ['U', 'D', 'L', 'R']:
                if move(board, players[currentPlayer], direction):
                    if is_game_over(players[currentPlayer]):
                        draw(board, players)
                        print(f"Player {players[currentPlayer]['symbol']} wins!")
                        break
                    currentPlayer = 1 - currentPlayer
                else:
                    print("Invalid move")
            else:
                print("Invalid direction")

        elif inp == 'W':
            x1, y1, x2, y2 = map(int, input("Two coordinates (e.g., '4 5 4 4'): ").split())
            if players[currentPlayer]['walls'] > 0 and place_wall(board, players[currentPlayer], x1, y1, x2, y2):
                currentPlayer = 1 - currentPlayer
            else:
                print("Invalid wall placement. Try again.")
        else:
            print("Invalid input. Enter 'M' or 'W'.")


if __name__ == "__main__":
    main()
