class Board:
    def __init__(self, ):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]

    def display_board(self):
        for row in self.board:
            print('|'.join(row))
            print('-' * 5)

    def make_move(self, row, col, symbol):
        if self.board[row][col] == ' ':
            self.board[row][col] = symbol
            return True
        return False
    
    def check_win(self, symbol):
        for i in range(3):
            win = True
            for j in range(3):
                if self.board[i][j] != symbol:
                    win = False
                    break
            if win:
                return win

        for j in range(3):
            win = True
            for i in range(3):
                if self.board[i][j] != symbol:
                    win = False
                    break
            if win:
                return win
        
        win = True
        # check diagonals
        for i in range(3):
            if self.board[i][i] != symbol:
                win = False
                break
        if win:
            return win
        win = True
        for i in range(3):
            if self.board[i][2 - i] != symbol:
                win = False
                break
        return win
    

    def is_full(self):
        for row in self.board:
            for cell in row:
                if cell == ' ':
                    return False
        return True
