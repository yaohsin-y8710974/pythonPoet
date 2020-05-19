class LineWrapper:
    def __init__(self, out, indent, column_limit):
        self.out = out
        self.indent = indent
        self.column_limit = column_limit

    @classmethod
    def wrapping_space(cls, indent_level):
        pass

    @classmethod
    def zero_width_space(cls, indent_level):
        pass

    @classmethod
    def append(cls, param):
        pass
