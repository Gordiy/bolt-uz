class ExcelLogger(object):
    """Logger for Exel parser."""
    info_patterns = {}
    error_patterns = {
        'no_excel': 'Помилка при імпорті файлу excel. Перевірте файл.',
        'only_headers': 'Файл не містить даних.',
    }

    def __init__(self):
        self._info = []
        self._errors = []

    @property
    def info(self):
        return self._info

    @property
    def errors(self):
        return self._errors

    def add_info(self, message: str) -> None:
        """
        Add info log.
        
        :param message: info log message.
        :return: None
        """
        self._info.append(message)

    def add_error(self, message) -> None:
        """
        Add error log.
        
        :param message: error log message.
        :return: None
        """
        self._errors.append(message)
