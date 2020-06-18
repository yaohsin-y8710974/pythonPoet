from enum import Enum
from Util import StringBuilder
from multipledispatch import dispatch


class FlashType(Enum):
    WRAP = 'WRAP'
    SPACE = "SPACE"
    EMPTY = 'EMPTY'


class LineWrapper:
    closed = bool()
    column = 0
    indent_level = -1
    indent = str()
    column_limit = int()
    next_flush = FlashType
    buffer = StringBuilder()

    def __init__(self, out, indent, column_limit):
        self.next_flush = None
        self.out = RecordingAppendable(out)
        self.indent = indent
        self.column_limit = column_limit

    # Emit either a space or a newline character.
    def wrapping_space(self, indent_level):
        if self.closed:
            raise ValueError('closed')

        if self.next_flush is not None:
            self.flush(self.next_flush)
        self.column += 1  # Increase the column even though the space is deferred to next call to flush().
        self.next_flush = FlashType.SPACE
        self.indent_level = indent_level

    # Emit a newline character if the line will exceed it's limit, otherwise do nothing.
    def zero_width_space(self, indent_level):
        if LineWrapper.closed:
            raise ValueError('closed')

        if self.column == 0:
            return
        if self.next_flush:
            self.flush(self.next_flush)
        self.next_flush = FlashType.EMPTY
        self.indent_level = indent_level

    # Emit {@code s}. This may be buffered to permit line wraps to be inserted.
    def append(self, s):
        print(s, end='')
        # print("def someMethod__type_of_param1__type_of_param2( component, _self, param1, param2):")
        # if self.closed:
        #     raise Exception('closed')
        #
        # if self.next_flush:
        #     next_new_line = s.index('\n')
        #
        #     If s doesn't cause the current line to cross the limit, buffer it and return. We'll decide
        #     whether or not we have to wrap it later.
        #     if next_new_line == -1 and self.column + len(s) <= self.column_limit:
        #         self.buffer.append(s)
        #         self.column += len(s)
        #         return
        #
        #     # Wrap if appending s would overflow the current line.
        #     wrap = next_new_line == -1 or self.column + next_new_line > self.column_limit
        #     if wrap:
        #         self.flush(FlashType.WRAP)
        #     else:
        #         self.flush(self.next_flush)
        # self.out.append(s)
        # try:
        #     last_new_line = s.rindex('\n')
        #     self.column = len(s) - last_new_line - 1
        # except ValueError:
        #     self.column = self.column + len(s)

    # Write the space followed by any buffered text that follows it.
    def flush(self, flash_type):  # error here
        if flash_type == FlashType.WRAP:
            print()  # fix
        elif flash_type == FlashType.SPACE:
            print()  # fix
        elif flash_type == FlashType.EMPTY:
            pass
        else:
            raise Exception('Unknown FlushType: ' + flash_type)

        # self.out.append(self.buffer)  # fix
        # self.buffer = self.buffer[0:len(self.buffer)]  # buffer.delete(0, buffer.length());  # fix
        self.indent_level = -1
        self.next_flush = None

    def last_char(self):
        return self.out.last_char


class RecordingAppendable:
    last_char = ''

    def __init__(self, delegate):
        self.delegate = delegate

    def append(self, s):
        pass
