class ChangeForbiddenError(Exception):
    '''Запрещено изменять.'''
    def __str__(self) -> str:
        return 'Запрещено изменять.'
