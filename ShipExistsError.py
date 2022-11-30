class ShipExistsError(Exception):
    '''Корабль уже добавлен.'''
    def __str__(self) -> str:
        return 'Корабль уже добавлен.'
