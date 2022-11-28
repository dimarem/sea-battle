from exceptions.ShipExistError import ShipExistError
from exceptions.ChangeForbiddenError import ChangeForbiddenError
from exceptions.CellsAllocationError import CellsAllocationError
from exceptions.ShipDislocationAreaError import ShipDislocationAreaError
from exceptions.ShootError import ShootError
from exceptions.CellCoordError import CellCoordError
from Cell import Cell
from Ship import Ship


class Board:
    '''Класс описывающий доску.

    Аргументы:
    display_ships - индикатор того, что нужно отображать корабли на доске.
    show_boundary - индикатор необходимости отображать границу вокруг корабля.

    Атрибуты экземпляра:
    min - минимально допустимая координата ячейки по оси X.
    max - максимально допустимая координата ячейки по оси Y.
    all_ships_are_sunken - индикатор потопления всех кораблей.

    Методы экземпляра:
    add_ship(ship: Ship) - добавить корабль на доску.
    process_shot(x: int, y: int) - обрабатывает выстрел по ячейке доски.
    print - вывести доску в консоль.
    '''
    _min = 0
    _max = 6

    def __init__(self, display_ships: bool = True, show_boundary: bool = False) -> None:
        self._cells = [[Cell(i, j) for i in range(self._min, self._max)]
                       for j in range(self._min, self._max)]
        self.display_ships = display_ships
        self.show_boundary = show_boundary
        self._ships = []

    @property
    def min(self) -> int:
        '''Минимально допустимая координата ячейки по оси X.'''
        return self._min

    @min.setter
    def min(self, value) -> None:
        raise ChangeForbiddenError

    @property
    def max(self) -> int:
        '''Максимально допустимая координата ячейки по оси Y.'''
        return self._max

    @max.setter
    def max(self, value) -> None:
        raise ChangeForbiddenError

    @property
    def all_ships_are_sunken(self) -> bool:
        '''Индикатор потопления всех кораблей.'''
        n = 0
        for ship in self._ships:
            if ship.sunken:
                n += 1
        return n == len(self._ships)

    @all_ships_are_sunken.setter
    def all_ships_are_sunken(self, value) -> None:
        raise ChangeForbiddenError

    def add_ship(self, ship: Ship) -> None:
        '''Добавить корабль на доску.

        Аргументы:
        ship - экземпляр класса корабля.
        '''
        if ship in self._ships:
            raise ShipExistError

        ship_cells, ship_boundary_cells = self._allocate_cells(ship)

        if len(ship_cells) < ship.length:
            raise CellsAllocationError('Для данного корабля не удалось выделить достаточное количество ячеек')

        if not self._area_is_acceptable(ship_cells + ship_boundary_cells):
            raise ShipDislocationAreaError

        ship.cells = ship_cells
        ship.boundary_cells = ship_boundary_cells
        self._ships.append(ship)

        if self.display_ships:
            for cell in ship_cells:
                cell.occupied = True

            if self.show_boundary:
                for cell in ship_boundary_cells:
                    cell.boundary = True

    def _allocate_cells(self, ship: Ship) -> tuple[list[Cell], list[Cell]]:
        '''Возвращает кортеж, в котором первый элемент это список ячеек доски,
        которые отводятся под корабль, а второй - список ячеек, которые к ниму примыкают.

        Аргументы:
        ship - экземпляр класса корабля.
        '''
        ship_cells = []
        ship_boundary_cells = []

        if ship.horizontal:
            try:
                for y in range(ship.bow['y'], ship.bow['y'] + ship.length):
                    cell = self._cells[ship.bow['x']][y]
                    ship_cells.append(cell)
            except IndexError:
                pass

            if len(ship_cells):
                i_start = -1 if ship.bow['x'] > 0 else 0

                for i in range(i_start, 2):
                    y_start = ship.bow['y'] - 1 if (ship.bow['y'] - 1) > 0 else 0

                    for y in range(y_start, ship.bow['y'] + ship.length + 1):
                        try:
                            cell = self._cells[ship.bow['x'] + i][y]
                            if cell not in ship_cells:
                                ship_boundary_cells.append(cell)
                        except IndexError:
                            pass
        else:
            try:
                for x in range(ship.bow['x'], ship.bow['x'] + ship.length):
                    cell = self._cells[x][ship.bow['y']]
                    ship_cells.append(cell)
            except IndexError:
                pass

            if len(ship_cells):
                for i in range(-1, 2):
                    for x in range(ship.bow['x'] - 1, ship.bow['x'] + ship.length + 1):
                        try:
                            cell = self._cells[x][ship.bow['y'] + i]
                            if cell not in ship_cells:
                                ship_boundary_cells.append(cell)
                        except IndexError:
                            pass

        return ship_cells, ship_boundary_cells

    @staticmethod
    def _area_is_acceptable(area_cells: list[Cell]) -> bool:
        '''Проверяет является ли область на доске допустимой для размещения корабля.

        Аргументы:
        area_cells - список ячеек проверяемой области.
        '''
        for cell in area_cells:
            if cell.occupied:
                return False
        return True

    def process_shot(self, x: int, y: int):
        '''Обрабатывает выстрел по ячейке доски.

        Аргументы:
        x - координата ячейки по оси X.
        y - координата ячейки по оси Y.
        '''
        _min = self._min + 1
        _max = self._max

        if x < _min or x > _max:
            raise CellCoordError(f'''Координата "x" должна быть от {_min} до {_max}''')

        elif y < _min or y > _max:
            raise CellCoordError(f'''Координата "y" должна быть от {_min} до {_max}''')

        cell = self._cells[x - 1][y - 1]

        if cell.shot:
            raise ShootError

        for ship in self._ships:
            if cell in ship.cells:
                cell.shot = True
                cell.missed = False
                ship.damage()

                if ship.sunken:
                    print('Потопил!')
                else:
                    print('Попал!')
            else:
                cell.shot = True
                print('Промазал!')

    def print(self) -> None:
        '''Вывести доску в консоль.'''
        print('  | 1 | 2 | 3 | 4 | 5 | 6 ')
        for i in range(self._min + 1, self._max + 1):
            print(f'{i} | {" | ".join(map(str, self._cells[i - 1]))}')


if __name__ == '__main__':
    # ------------------------ Экземпляр класса ------------------------
    board = Board()
    min = board.min
    max = board.max
    all_ships_are_sunken = board.all_ships_are_sunken

    try:
        board.min = 123
    except ChangeForbiddenError:
        pass

    try:
        board.max = 123
    except ChangeForbiddenError:
        pass

    try:
        board.all_ships_are_sunken = 'True'
    except ChangeForbiddenError:
        pass

    assert board.min == min
    assert board.max == max
    assert board.all_ships_are_sunken == all_ships_are_sunken

    # ------------------------ Отображение доски ------------------------
    # длина корабля
    # если выйдет за пределы доски будет выбражено исключение
    ship_length = 1
    # индикатор необходимости выделить точки примыкающие к кораблю (B)
    show_boundary = True

    print()

    coords = [(0, 0), (1, 0), (1, 1), (0, 1),
              (0, 5), (1, 5), (1, 4), (0, 4),
              (5, 0), (5, 5), (2, 2), (1, 3)]

    for coord in coords:
        print('=' * 50)
        print(f'Координаты носа корабля: {coord}. Длина корабля: {ship_length}.')
        print()
        board = Board(show_boundary=show_boundary)
        ship = Ship({'x': coord[0], 'y': coord[1]}, ship_length)
        board.add_ship(ship)
        board.print()
        print()

    print('=' * 50)
    print('Координаты носа корабля: (1, 3). Длина корабля: 3.')
    print('Вертикальный вариант.')
    print()
    board = Board(show_boundary=show_boundary)
    ship = Ship({'x': 1, 'y': 3}, 3, horizontal=False)
    board.add_ship(ship)
    board.print()
    print()

    print()

    print('=' * 50)
    print('Координаты носа корабля: (0, 0). Длина корабля: 3.')
    print('Корабль не отображен.')
    print()
    board = Board(display_ships=False)
    ship = Ship({'x': 0, 'y': 0}, 3)
    board.add_ship(ship)
    board.print()

    print()

    print('=' * 50)
    print('Координаты носа корабля: (1, 3). Длина корабля: 6.')
    print('Корабль выходит за пределы доски. Должно быть выбрашено исключение.')
    print()
    board = Board(show_boundary=show_boundary)
    ship = Ship({'x': 1, 'y': 3}, 6)
    try:
        board.add_ship(ship)
        board.print()
    except CellsAllocationError as e:
        print(f'Исключение: "{e}"')
    print()

    print('=' * 50)
    print('Координаты носа первого корабля: (1, 1). Длина корабля: 3.')
    print('Координаты носа второго корабля: (3, 2). Длина корабля: 1.')
    print()
    board = Board(show_boundary=show_boundary)
    ship_1 = Ship({'x': 1, 'y': 1}, 3)
    ship_2 = Ship({'x': 3, 'y': 2}, 1)
    board.add_ship(ship_1)
    board.add_ship(ship_2)
    board.print()

    print()

    print('=' * 50)
    print('Координаты носа первого корабля: (1, 1). Длина корабля: 3.')
    print('Координаты носа второго корабля: (1, 1). Длина корабля: 1.')
    print('Корабли пересекаются. Должно быть выбрашено исключение.')
    print()
    board = Board(show_boundary=show_boundary)
    ship_1 = Ship({'x': 1, 'y': 1}, 3)
    ship_2 = Ship({'x': 1, 'y': 1}, 1)
    try:
        board.add_ship(ship_1)
        board.add_ship(ship_2)
        board.print()
    except ShipDislocationAreaError as e:
        print(f'Исключение: "{e}"')
    print()

    print('=' * 50)
    print('Координаты носа первого корабля: (1, 1). Длина корабля: 3.')
    print('Координаты носа второго корабля: (2, 1). Длина корабля: 1.')
    print('Корабли соприкасаются по вертикали. Должно быть выбрашено исключение.')
    print()
    board = Board(show_boundary=show_boundary)
    ship_1 = Ship({'x': 1, 'y': 1}, 3)
    ship_2 = Ship({'x': 2, 'y': 1}, 1)
    try:
        board.add_ship(ship_1)
        board.add_ship(ship_2)
        board.print()
    except ShipDislocationAreaError as e:
        print(f'Исключение: "{e}"')
    print()

    print('=' * 50)
    print('Координаты носа первого корабля: (1, 1). Длина корабля: 3.')
    print('Координаты носа второго корабля: (1, 4). Длина корабля: 1.')
    print('Корабли соприкасаются по горизонтали. Должно быть выбрашено исключение.')
    print()
    board = Board(show_boundary=show_boundary)
    ship_1 = Ship({'x': 1, 'y': 1}, 3)
    ship_2 = Ship({'x': 1, 'y': 4}, 1)
    try:
        board.add_ship(ship_1)
        board.add_ship(ship_2)
        board.print()
    except ShipDislocationAreaError as e:
        print(f'Исключение: "{e}"')
    print()

    print('=' * 50)
    print('Координаты носа корабля: (0, 0). Длина корабля: 3.')
    print('Выстрел в точку с координатами: (0, 0).')
    print()
    board = Board(show_boundary=show_boundary)
    ship = Ship({'x': 0, 'y': 0}, 3)
    board.add_ship(ship)
    # система координат для пользователя начинается с 1
    board.process_shot(1, 1)
    board.print()

    print('=' * 50)
    print('Координаты носа корабля: (0, 0). Длина корабля: 3.')
    print('Выстрел в точки с координатами: (0, 0), (0, 1), (0, 2).')
    print()
    board = Board(show_boundary=show_boundary)
    ship = Ship({'x': 0, 'y': 0}, 3)
    board.add_ship(ship)
    # система координат для пользователя начинается с 1
    board.process_shot(1, 1)
    board.process_shot(1, 2)
    board.process_shot(1, 3)
    board.print()

    print('=' * 50)
    print('Координаты носа корабля: (0, 0). Длина корабля: 3.')
    print('Повторный выстрел в точку с координатами: (0, 0).  Должно быть выбрашено исключение.')
    print()
    board = Board(show_boundary=show_boundary)
    ship = Ship({'x': 0, 'y': 0}, 3)
    board.add_ship(ship)
    try:
        # система координат для пользователя начинается с 1
        board.process_shot(1, 1)
        board.process_shot(1, 1)
    except ShootError as e:
        print(e)
    board.print()

    print('=' * 50)
    print('Координаты носа корабля: (0, 0). Длина корабля: 3.')
    print('Выстрел в точку с координатами: (2, 4).')
    print()
    board = Board(show_boundary=show_boundary)
    ship = Ship({'x': 0, 'y': 0}, 3)
    board.add_ship(ship)
    # система координат для пользователя начинается с 1
    board.process_shot(2, 4)
    board.print()

    print()

    print('=' * 50)
    print('Выстрел в точку с координатами: (-1, 4).')
    print()
    board = Board()
    try:
        # система координат для пользователя начинается с 1
        board.process_shot(-1, 4)
        board.print()
    except CellCoordError as e:
        print(e)

    print()

    print('=' * 50)
    print('Выстрел в точку с координатами: (1, 14).')
    print()
    board = Board()
    try:
        # система координат для пользователя начинается с 1
        board.process_shot(1, 14)
        board.print()
    except CellCoordError as e:
        print(e)

    print()
