class ShipDislocationAreaError(Exception):
    '''Недопустимая область для размещения корабля.'''
    def __str__(self) -> str:
        return 'Недопустимая область для размещения корабля.'
