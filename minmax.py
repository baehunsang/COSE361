class Game:
    def __init__(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'

    def display_board(self):
        for row in self.board:
            print('|'.join(row))
            print('-' * 5)

    def make_move(self, row, col):
        if self.board[row][col] == ' ':
            self.board[row][col] = self.current_player
            self.current_player = 'O' if self.current_player == 'X' else 'X'
            return True
        return False

    def check_winner(self, player):
        for row in range(3):
            if all([cell == player for cell in self.board[row]]):
                return True
        for col in range(3):
            if all([self.board[row][col] == player for row in range(3)]):
                return True
        if all([self.board[i][i] == player for i in range(3)]):
            return True
        if all([self.board[i][2 - i] == player for i in range(3)]):
            return True
        return False

    def is_draw(self):
        return all([cell != ' ' for row in self.board for cell in row])

    def is_game_over(self):
        return self.check_winner('X') or self.check_winner('O') or self.is_draw()
    
    def minimax(self, is_maximizing_player, player):
        if self.check_winner('X'):
            return -1
        if self.check_winner('O'):
            return 1
        if self.is_draw():
            return 0

        best_value = -float('inf') if is_maximizing_player else float('inf')

        for row in range(3):
            for col in range(3):
                if self.board[row][col] == ' ':
                    self.board[row][col] = player
                    next_player = 'O' if player == 'X' else 'X'
                    value = self.minimax(not is_maximizing_player, next_player)
                    self.board[row][col] = ' '

                    if is_maximizing_player:
                        best_value = max(best_value, value)
                    else:
                        best_value = min(best_value, value)

        return best_value

    #Minmax initial max call
    def find_best_move(self):
        best_value = -float('inf')
        best_move = None

        for row in range(3):
            for col in range(3):
                if self.board[row][col] == ' ':
                    self.board[row][col] = 'O'
                    move_value = self.minimax(False, 'X')
                    self.board[row][col] = ' '

                    if move_value > best_value:
                        best_value = move_value
                        best_move = (row, col)

        return best_move

def main():
    game = Game()

    while not game.is_game_over():
        game.display_board()

        if game.current_player == 'X':
            row, col = map(int, input("Enter your move (row, col): ").split(','))
            game.make_move(row, col)
        else:
            row, col = game.find_best_move()
            print(f"Computer's move: {row}, {col}")
            game.make_move(row, col)

    game.display_board()

    if game.check_winner('X'):
        print("You win!")
    elif game.check_winner('O'):
        print("Computer wins!")
    else:
        print("It's a draw!")


if __name__ == "__main__":
    main()