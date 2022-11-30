class BoardCreationError(Exception):
    '''Неудачная попытка создания доски.'''
    def __str__(self) -> str:
        return 'Не удалось создать доску для игры.'
