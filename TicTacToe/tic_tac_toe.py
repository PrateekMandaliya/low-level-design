from player import Player
from board import Board

class TicTacToe:
    def __init__(self, player1_name, player2_name):
        self.player1 = Player(player1_name, 'X')
        self.player2 = Player(player2_name, 'O')
        self.board = Board()
        self.current_player = self.player1

    def switch_player(self):
        self.current_player = self.player2 if self.current_player == self.player1 else self.player1

    def start_game(self):
        while True:
            self.board.display_board()
            print(f'{self.current_player.name}\'s turn:')
            row = int(input('Enter row(0, 1, 2): '))
            col = int(input('Enter column(0, 1, 2): '))

            if self.board.make_move(row, col, self.current_player.symbol):
                if self.board.check_win(self.current_player.symbol):
                    self.board.display_board()
                    print(f"Congratulations! {self.current_player.name} wins!")
                    break
                elif self.board.is_full():
                    self.board.display_board()
                    print('It\'s a draw')
                    break
                self.switch_player()

            else:
                print('Invalid move. Please try again!')


#  Running the game
game1 = TicTacToe('Prateek', 'Neha')
game1.start_game()

