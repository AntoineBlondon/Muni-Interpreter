from muni_context_manager import *

class Muni_Error(Exception):
    def __init__(self, message, lineno=None, col_offset=None):
        super().__init__(message)
        self.message = message
        self.context = ContextManager()
        self.line = self.context.get_lineno() if lineno is None else lineno
        self.column = col_offset

    def __str__(self):
        location_info = ""
        if self.line is not None:
            location_info = f" at line {self.line}"
            if self.column is not None:
                location_info += f", column {self.column}"

        return f"Muni Error{location_info}: {self.message}"
