class InvalidCoordsError(Exception):
    '''Неверно введены координаты ячейки.'''
    def __str__(self) -> str:
        return 'Неверно введены координаты ячейки.'
