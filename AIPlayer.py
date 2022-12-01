from random import randint
from Board import Board


class AIPlayer:
    '''Класс описывающий игрока ИИ.

    Аргументы:
    min_coord - минимальная координата для совершения выстрела.
    max_coord - максимальная координата для совершения выстрела.
    '''
    def __init__(self, min_coord: int, max_coord: int) -> None:
        self._min_coord = min_coord
        self._max_coord = max_coord
        # координаты совершенных ранее выстрелов
        self._coords = []

    def shoot(self) -> tuple[int, int]:
        '''Совершить выстрел и запомнить его данные.'''
        while True:
            x = randint(self._min_coord, self._max_coord)
            y = randint(self._min_coord, self._max_coord)
            coords = (x, y)

            if coords in self._coords:
                continue
            else:
                self._coords.append(coords)
                return coords


if __name__ == '__main__':
    board = Board()
    ai = AIPlayer(board.min, board.max)

    coords = ai.shoot()
    print(coords)

    assert coords in ai._coords
