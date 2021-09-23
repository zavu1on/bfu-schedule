import logging
from rich import logging as rich_logging


class ConsoleHandler(logging.Handler):

    def emit(self, record: logging.LogRecord):
        report = f'{record.module} {record.message}'

        if record.levelname == 'INFO':
            color = 'blue'
        else:
            color = 'yellow'

        console = rich_logging.Console()
        console.print(f'[bold {color}]{record.levelname}[/bold {color}] {report}')
