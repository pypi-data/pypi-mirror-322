from bunch_py3 import Bunch
import inspect
import linecache
import itertools


class CodeCapture:
    key: str
    store = Bunch()

    def __init__(self, key):
        self.key = key

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        cf = inspect.currentframe().f_back
        filename = cf.f_code.co_filename
        line_number = cf.f_lineno
        lines = []
        indent = None

        for i in itertools.count(start=1):
            line = linecache.getline(filename, line_number + i)
            line_indent = len(line) - len(line.lstrip())

            if indent is None:
                indent = line_indent
            elif (line_indent < indent and len(line.strip()) > 0) or line == "":
                break

            if line == "\n":  # preserve newlines
                lines.append(line)
            else:
                lines.append(line[indent:])

        content = "".join(lines)
        self.store[self.key] = content
