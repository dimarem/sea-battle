from random import randint
import sys
from BoardCreationError import BoardCreationError
from ShipExistsError import ShipExistsError
from CellsAllocationError import CellsAllocationError
from ShipDislocationAreaError import ShipDislocationAreaError
from InvalidCoordsError import InvalidCoordsError
from ShootError import ShootError
from CellCoordsError import CellCoordsError
from Board import Board
from Ship import Ship
from AIPlayer import AIPlayer


class Controller:
    '''Класс описывающий контроллера игрового процесса.'''
    def __init__(self) -> None:
        # количество попыток для создания игровых досок
        self._attempt = 3
        # доска пользователя
        self._human_board = None
        # доска ИИ
        self._ai_board = None
        # True - ход игрока, False - ИИ
        self._human_step = True

    def start_game(self):
        '''Начинает игру.'''
        self._setup()
        self._show_greeting()
        self.print_boards()

        while True:
            if self._human_step:
                try:
                    print('=' * 25 + ' ВЫ ' + '=' * 25)
                    coords = self._get_cell_coords()

                    if len(coords) != 2:
                        raise InvalidCoordsError

                    print(f'Вы стреляете по ячейке с координатами ({coords[0]}, {coords[1]})')

                    try:
                        self._ai_board.process_shot(coords[0], coords[1])
                        self._human_step = False

                        if self._ai_board.all_ships_are_sunken:
                            print('Вы выиграли!')
                            break
                    except (ShootError, CellCoordsError) as e:
                        print(e)
                except InvalidCoordsError as e:
                    print(e)
                except Exception:
                    print('В время игры возникла непредвиденная ошибка.')
                    print('Выход.')
                    break
            else:
                print('=' * 25 + ' ИИ ' + '=' * 25)
                coords = self._ai_player.shoot()
                print(f'ИИ стреляет по ячейке с координатами ({coords[0]}, {coords[1]})')
                self._human_board.process_shot(coords[0], coords[1])
                self._human_step = True

                if self._human_board.all_ships_are_sunken:
                    print('ИИ выиграл. В следующий раз повезет больше.')
                    break

            if self._ai_board.all_cells_are_shot or self._human_board.all_cells_are_shot:
                print('Ничья')
                break

            self.print_boards()

    def _setup(self):
        '''Формирует и заполняет доски для пользователя и ИИ.'''
        try:
            self._create_human_board()
            self._create_ai_board()
            self._ai_player = AIPlayer(self._ai_board.min, self._ai_board.max)
        except BoardCreationError as e:
            if self._attempt:
                self._attempt -= 1
                self._setup()
            else:
                print(e)
                sys.exit()

    def _get_cell_coords(self) -> list[int, int]:
        '''Получить координаты выстрела.'''
        _input = input('Введите координаты выстрела: ')
        coords = list(map(int, _input.split()))

        return coords

    def _create_human_board(self) -> None:
        '''Создает доску для пользователя.'''
        human_board = Board()

        # 1 корабль на 3 клетки
        n = 1000
        while n:
            x = randint(human_board.min, human_board.max)
            y = randint(human_board.min, human_board.max)
            bow = {'x': x, 'y': y}
            length = 3
            horizontal = True if randint(0, 1) else False
            ship = Ship(bow=bow, length=length, horizontal=horizontal)

            try:
                human_board.add_ship(ship)
                break
            except (ShipExistsError, CellsAllocationError, ShipDislocationAreaError):
                n -= 1

            if not n:
                raise BoardCreationError

        # 2 корабля на 2 клетки
        for i in range(2):
            n = 1000
            while n:
                x = randint(human_board.min, human_board.max)
                y = randint(human_board.min, human_board.max)
                bow = {'x': x, 'y': y}
                length = 2
                horizontal = True if randint(0, 1) else False
                ship = Ship(bow=bow, length=length, horizontal=horizontal)

                try:
                    human_board.add_ship(ship)
                    break
                except (ShipExistsError, CellsAllocationError, ShipDislocationAreaError):
                    n -= 1

                if not n:
                    raise BoardCreationError

        # 4 корабля на одну клетку
        for i in range(4):
            n = 1000
            while n:
                x = randint(human_board.min, human_board.max)
                y = randint(human_board.min, human_board.max)
                bow = {'x': x, 'y': y}
                length = 1
                ship = Ship(bow=bow, length=length)

                try:
                    human_board.add_ship(ship)
                    break
                except (ShipExistsError, CellsAllocationError, ShipDislocationAreaError):
                    n -= 1

                if not n:
                    raise BoardCreationError

        self._human_board = human_board

    def _create_ai_board(self) -> None:
        '''Создает доску для ИИ.'''
        ai_board = Board(display_ships=False)

        # 1 корабль на 3 клетки
        n = 1000
        while n:
            x = randint(ai_board.min, ai_board.max)
            y = randint(ai_board.min, ai_board.max)
            bow = {'x': x, 'y': y}
            length = 3
            horizontal = True if randint(0, 1) else False
            ship = Ship(bow=bow, length=length, horizontal=horizontal)

            try:
                ai_board.add_ship(ship)
                break
            except (ShipExistsError, CellsAllocationError, ShipDislocationAreaError):
                n -= 1

            if not n:
                raise BoardCreationError

        # 2 корабля на 2 клетки
        for i in range(2):
            n = 1000
            while n:
                x = randint(ai_board.min, ai_board.max)
                y = randint(ai_board.min, ai_board.max)
                bow = {'x': x, 'y': y}
                length = 2
                horizontal = True if randint(0, 1) else False
                ship = Ship(bow=bow, length=length, horizontal=horizontal)

                try:
                    ai_board.add_ship(ship)
                    break
                except (ShipExistsError, CellsAllocationError, ShipDislocationAreaError):
                    n -= 1

                if not n:
                    raise BoardCreationError

        # 4 корабля на одну клетку
        for i in range(4):
            n = 1000
            while n:
                x = randint(ai_board.min, ai_board.max)
                y = randint(ai_board.min, ai_board.max)
                bow = {'x': x, 'y': y}
                length = 1
                ship = Ship(bow=bow, length=length)

                try:
                    ai_board.add_ship(ship)
                    break
                except (ShipExistsError, CellsAllocationError, ShipDislocationAreaError):
                    n -= 1

                if not n:
                    raise BoardCreationError

        self._ai_board = ai_board

    def _show_greeting(self) -> None:
        '''Отображает приветствие и правила игры.'''
        print('-' * 100)
        print()
        print('Добро пожаловать в игру "Морской бой"!')
        print()
        print('Правила игры:')
        print()
        print('1. Корабль на вашей доске отображается в виде точки.')
        print('2. Для совершения выстрела введите в консоль координаты ячейки ввиде двух чисел, например: 1 2.')
        print('3. Промах отметачется буквой "T", попадание - "X".')
        print('4. Победит тот, кто первым потопит корабли противника.')
        print()
        print('Удачи!')

    def print_boards(self) -> None:
        '''Печатает доски в консоль.'''
        print()
        print('Ваша доска:')
        self._human_board.print()
        print()
        print('Доска ИИ:')
        self._ai_board.print()
        print()


if __name__ == '__main__':
    controller = Controller()
    controller._setup()
    controller.print_boards()
