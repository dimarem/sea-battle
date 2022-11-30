class Cell:
    '''Класс описывающий ячейку на доске.

    Аргументы:
    x - координата ячейки по оси X.
    y - координата ячейки по оси Y.

    Атрибуты экземпляра:
    x - координата ячейки по оси X.
    y - координата ячейки по оси Y.
    shot - индикатор того, что по ячейке бы произведен выстрел.
    missed - индикатор того, что попадания по кораблю не было.
    occupied - индикатор того, что ячейка занята кораблем.
    boundary - индикатор того, что ячейка примыкает к кораблю.
    displayed - индикатор того, что ячейка корабля отображена.
    '''
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.shot = False
        self.missed = True
        self.occupied = False
        self.boundary = False
        self.displayed = False

    def __eq__(self, other) -> bool:
        if self.x == other.x and self.y == other.y:
            return True
        else:
            return False

    def __str__(self) -> str:
        if self.displayed and self.occupied and not self.shot:
            return '.'
        elif self.occupied and self.shot and not self.missed:
            return 'X'
        elif not self.occupied and self.shot and self.missed:
            return 'T'
        elif self.boundary:
            return 'B'
        else:
            return 'O'


if __name__ == '__main__':
    cell_1 = Cell(1, 1)
    cell_2 = Cell(1, 1)
    cell_3 = Cell(1, 2)
    cell_4 = Cell(2, 1)

    assert cell_1 == cell_2
    assert cell_1 != cell_3
    assert cell_1 != cell_4
