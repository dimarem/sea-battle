class CellsAllocationError(Exception):
    '''Не удалось выделить достаточное количество ячеек.'''
    def __str__(self) -> str:
        return 'Не удалось выделить достаточное количество ячеек.'
