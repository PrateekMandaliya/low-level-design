class Player:
    def __init__(self, name):
        self.name = name
        self.position = 1

    def move(self, new_position):
        self.position = new_position

    def __str__(self):
        return f"{self.name} at {self.position}"
    

import random

class Dice:
    def __init__(self, faces=6):
        self.faces = faces

    def roll(self):
        return random.randint(1, self.faces)
    

class MovingEntity:
    """
    You can create any moving entity , like snake or ladder or
    wormhole by extending this 
    """
    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end

    def apply_position(self, position: int) -> int:
        """Apply movement if applicable"""
        if self.start == position:
            return self.end
        return position
    
    def __str__(self):
        return f"{self.__class__.__name__} from {self.start} to {self.end}"
    

class Snake(MovingEntity):
    def __init__(self, head: int, tail: int):
        assert head > tail, "Snake head must be higher than tail"
        super().__init__(head, tail)


class Ladder(MovingEntity):
    def __init__(self, bottom: int, top: int):
        assert bottom < top, "Ladder must go up"
        super().__init__(bottom, top)


class Cell:
    def __init__(self):
        self.entity: MovingEntity | None = None

    def set_entity(self, entity: MovingEntity):
        self.entity = entity

    """ ALLOWS ME O(1) RETRIEVAL IF MY NEW POSITION IS A SNAKE / LADDER"""
    def get_entity(self):
        return self.entity
    

from typing import List

class Board:
    def __init__(self, size: int, entities: List[MovingEntity]):
        self.size = size
        self.cells = [Cell() for _ in range(size + 1)]   # 1-based index

        for entity in entities:
            self.cells[entity.start].set_entity(entity)
    
    def apply_movement(self, position: int) -> int:
        while True:
            cell = self.cells[position]
            entity = cell.get_entity()
            if entity:
                new_pos = entity.apply_position(position)
                if new_pos != position:
                    print(f"Hit {entity}. Moving to {new_pos}")
                    position = new_pos
                    continue
            break
        return position


from collections import deque

class GameController:
    def __init__(self, board: Board, players: list[Player], dice: Dice):
        self.board = board
        self.dice = dice
        # Make players as a queue, in order to support pop from left and push to right
        self.players = deque(players)
        self.game_over = False

    def simulate_game(self):
        while not self.game_over:
            current_player = self.players.popleft()
            print(f"\n🎲 {current_player.name}'s turn")

            roll = self.dice.roll()
            print(f"Rolled: {roll}")

            next_pos = current_player.position + roll
            if next_pos > self.board.size:
                print(f"Can't move beyond {self.board.size}. Staying at {current_player.position}")
            else:
                final_pos = self.board.apply_movement(next_pos)
                current_player.move(final_pos)
                print(f"{current_player.name} moved to {final_pos}")

                if final_pos == self.board.size:
                    self.game_over = True
                    print(f"\n🏆 {current_player.name} wins the game!")
                    return
            
            self.players.append(current_player)


if __name__ == "__main__":
    # Define entities: snakes and ladders
    entities = [
        Snake(17, 7),
        Snake(54, 34),
        Snake(62, 19),
        Snake(98, 79),
        Ladder(3, 22),
        Ladder(5, 8),
        Ladder(11, 26),
        Ladder(20, 29),
        Ladder(27, 84)
    ]

    # Create board, players, dice
    board = Board(size=100, entities=entities)
    players = [Player("Alice"), Player("Bob")]
    dice = Dice()

    # Start game
    game = GameController(board, players, dice)
    game.simulate_game()
