class ShipExistError(Exception):
    '''Корабль уже добавлен.'''
    def __str__(self) -> str:
        return 'Корабль уже добавлен.'
