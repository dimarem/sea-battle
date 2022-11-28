from exceptions .ChangeForbiddenError import ChangeForbiddenError


class Ship:
    '''Класс описывающий корабль на доске.

    Аргументы:
    bow - словарь вида {'x': 0, 'y': 0}, где x и y координаты носа корабля на доске.
    length - длина корабля.
    horizontal - расположение корабля.

    Атрибуты экземпляра:
    bow - словарь вида {'x': 0, 'y': 0}, где x и y координаты носа корабля на доске.
    length - длина корабля.
    horizontal - расположение корабля.
    cells - список ячеек, которые занимает корабль.
    boundary_cells - список ячеек, которые примыкают к кораблю.
    sunken - индикатор потопления корабля.

    Методы экземпляра:
    damage - отнимает одну жизнь у корабля.
    '''
    def __init__(self, bow: dict, length: int, horizontal: bool = True) -> None:
        self.bow = bow
        self.length = length
        self.horizontal = horizontal
        self.cells = []
        self.boundary_cells = []
        self._lives = length

    def damage(self) -> None:
        '''Отнимает одну жизнь у корабля.'''
        if self._lives > 0:
            self._lives -= 1

    @property
    def sunken(self) -> bool:
        '''Проверяет потоплен ли текущий корабль.'''
        if self._lives:
            return False
        else:
            return True

    @sunken.setter
    def sunken(self, value) -> None:
        raise ChangeForbiddenError


if __name__ == '__main__':
    bow = {'x': 1, 'y': 2}
    length = 2
    ship = Ship(bow, length)

    assert ship.sunken is False

    try:
        ship.sunken = True
    except Exception:
        pass

    assert ship.sunken is False

    ship.damage()
    ship.damage()

    assert ship.sunken is True
