import sys
from datetime import datetime, timedelta, timezone
from functools import wraps
from html import escape
from logging import Formatter, Logger, StreamHandler, addLevelName, getLevelNamesMapping, getLogger
from logging.handlers import RotatingFileHandler
from os import name as os_name
from pathlib import Path
from re import search
from site import getsitepackages

RED = '\033[01;38;05;167m'
GREEN = '\033[01;38;05;77m'
BLUE = '\033[01;38;05;74m'
LIGHTBLUE = '\033[38;05;116m'
ORANGE = '\033[01;38;05;173m'
YELLOW = '\033[01;38;05;185m'
LIME = '\033[01;38;05;113m'
VIOLET = '\033[01;38;05;140m'
PINK = '\033[01;38;05;168m'
GRAY = '\033[01;38;05;247m'
DIM = '\033[38;05;246;48;05;232m'
TRACE = '\033[38;05;144;48;05;232m'
USUAL = '\033[m'

HTML_LOG_HEAD = '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>логи</title><style>html, body{background-color:#1d1e22; color:#c1beb4; font-family: monospace;}div{white-space: pre-line;}.start{color:#97b270}.msg{color:#70a9b2;}.error{font-weight: bolder; color:#b27070;}.trace{color:#b29e9e;}</style></head><body>'


class GetLog:
    def __init__(self, log_file: Path | str | None = None, logging_level: str = 'WARN'):
        lvls_map = getLevelNamesMapping()
        if log_file:
            self.log_file = Path(log_file)
            self.log_file.parent.mkdir(parents=True, exist_ok=True)
        self.logging_level = logging_level
        self.log_lvl = lvls_map.get(self.logging_level, 'DEBUG')

        colors = {
            'ПРЕДУПРЕЖДЕНИЕ': YELLOW,
            'ОШИБКА': RED,
            'ОПАСНОСТЬ': ORANGE,
            'ИНФОРМАЦИЯ': BLUE,
            'ОТЛАДКА': GRAY,
            'СОБЫТИЕ': LIGHTBLUE,
            'ТЕКСТ': USUAL
        }

        class ColoredFormatter(Formatter):

            def formatTime(self, record, datefmt=None):
                return DIM + super().formatTime(record, datefmt) + USUAL

            def format(self, record):
                level_name = record.levelname
                if level_name in colors:
                    if record.stack_info:
                        record.stack_info = TRACE + '=' * 12 + '\n' + record.stack_info + USUAL
                    record.levelname = colors[level_name] + level_name + USUAL
                    record.msg = colors[level_name].replace('01;', '') + record.msg + USUAL
                return super().format(record)

        event_level = 35
        self.event_level = event_level

        def event(self, message, *args, **kwargs):
            if self.isEnabledFor(event_level):
                self._log(event_level, message, args, **kwargs)

        self.logger = getLogger()
        self.logger.setLevel(self.log_lvl)
        addLevelName(lvls_map.get('WARNING'), 'ПРЕДУПРЕЖДЕНИЕ')
        addLevelName(lvls_map.get('ERROR'), 'ОШИБКА')
        addLevelName(lvls_map.get('CRITICAL'), 'ОПАСНОСТЬ')
        addLevelName(lvls_map.get('INFO'), 'ИНФОРМАЦИЯ')
        addLevelName(lvls_map.get('DEBUG'), 'ОТЛАДКА')
        Logger.event = event
        addLevelName(self.event_level, "СОБЫТИЕ")

        class UsualFormatter(Formatter):
            def format(self, record):
                if record.args:
                    record.msg = str(record.msg).format(*record.args)
                return super().format(record)

        if log_file:
            file_format = UsualFormatter('%(asctime)s | %(levelname)s : %(message)s', datefmt='%d.%m.%Y %H:%M:%S')
            file_format.converter = lambda *args: datetime.now(timezone(timedelta(hours=3))).timetuple()
            file_handler = RotatingFileHandler(log_file, maxBytes=1000000, backupCount=10, encoding='utf-8')
            file_handler.setLevel(self.log_lvl)
            file_handler.setFormatter(file_format)
            self.logger.addHandler(file_handler)

        console_format = ColoredFormatter('%(asctime)s | %(levelname)s : %(message)s', datefmt='%d.%m.%Y %H:%M:%S')
        console_format.converter = lambda *args: datetime.now(timezone(timedelta(hours=3))).timetuple()
        console_handler = StreamHandler(sys.stdout)
        console_handler.setLevel(self.log_lvl)
        console_handler.setFormatter(console_format)
        self.logger.addHandler(console_handler)

        self.debug = self.logger.debug
        self.info = self.logger.info
        self.event = self.logger.event
        self.warn = self.logger.warning
        self.error = self.logger.error
        self.crit = self.logger.critical
        self.exception = self.logger.exception
        sys.excepthook = self.handle_exception

    def handle_exception(self, exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return

        self.logger.error("ПОЛНЫЙ ПРОЛАПС", exc_info=(exc_type, exc_value, exc_traceback), stack_info=True)

    def exception_handler_decorator(self):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except Exception as exc:
                    self.logger.error(f'ПОЛНЫЙ ПРОЛАПС\nв {func.__name__}:\n{exc}', exc_info=True, stack_info=True)
                    return None

            return wrapper

        return decorator

    def log_to_html(self, log_file: Path | None = None, return_string: bool = True) -> str | Path:
        if not self.log_file and not log_file.is_file():
            raise ValueError(f'при создании экземпляра логгера ему не был переда путь до файла для сохранения логов, а {log_file.as_posix()} не существует.')
        log_file = self.log_file if not log_file else log_file
        for filename in log_file.parent.iterdir():
            if filename.suffix == '.html':
                filename.unlink()

        with open(log_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        start_index = 0
        for i in range(len(lines) - 1, -1, -1):
            if "СТАРТ: " in lines[i]:
                start_index = i - 1
                break
        html_lines = [f"{HTML_LOG_HEAD}<div class='lvl'>{log_file.stem} | уровень логгирования: {self.logging_level}</div>"]
        trace_flag = False
        msg_flag = False
        for line in lines[start_index:]:
            line = escape(line)
            if "СТАРТ: " in line:
                if msg_flag:
                    html_lines.append('</div>\n')
                    msg_flag = False
                html_lines.append('<div class="start">\n')
                html_lines.append(lines[start_index])
                html_lines.append(line)
                html_lines.append(lines[start_index + 2])
                html_lines.append('</div>\n')
            elif "ПРЕДУПРЕЖДЕНИЕ : " in line or "ИНФОРМАЦИЯ : " in line or "ОТЛАДКА : " in line or "ОПАСНОСТЬ : " in line:

                if msg_flag:
                    html_lines.append('</div>\n')
                    msg_flag = False
                if trace_flag:
                    html_lines.append('</div>\n')
                    trace_flag = False
                if "ПРЕДУПРЕЖДЕНИЕ : " in line:
                    html_lines.append('<div class="warn">' + line + '</div>\n')
                elif "ИНФОРМАЦИЯ : " in line:
                    html_lines.append('<div class="info">' + line + '</div>\n')
                elif "ОТЛАДКА : " in line:
                    html_lines.append('<div class="debug">' + line + '</div>\n')
                elif "ОПАСНОСТЬ : " in line:
                    html_lines.append('<div class="crit">' + line + '</div>\n')
            elif "ОШИБКА : " in line:
                if msg_flag:
                    html_lines.append('</div>\n')
                    msg_flag = False
                if trace_flag:
                    html_lines.append('</pre></div>\n')
                    trace_flag = False
                html_lines.append('<div class="error">' + line + '</div>\n<div class="trace"><pre>')
                trace_flag = True
            elif trace_flag and not search(r'\s\|\s', line):
                html_lines.append(line)
            else:
                if trace_flag:
                    html_lines.append('</div>\n')
                    trace_flag = False
                if not msg_flag and not search(r'----+', line):
                    html_lines.append('<div class="msg">\n' + line)
                    msg_flag = True
                elif not search(r'----+', line):
                    html_lines.append(line)
        if msg_flag:
            html_lines.append('</div>\n')
        if trace_flag:
            html_lines.append('</div>\n')
        html_lines.append('</body></html>')
        html_code = []
        for line in html_lines:
            for pip_path in getsitepackages():
                line = line.replace(pip_path[0].upper() + pip_path[1:].replace('\\\\', '\\') if os_name == 'nt' else pip_path, '...')
            html_code.append(line)
        if return_string:
            return '\n'.join(html_code)
        current_time = datetime.now(timezone(timedelta(hours=3))).strftime('%d.%m.%Y_%H-%M-%S')
        last_log_html = log_file.parent / f'{log_file.stem}_{current_time}.html'
        last_log_html.write_text(''.join(html_code), encoding='utf-8')
        return last_log_html
