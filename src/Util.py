import io


class StringBuilder(object):
    def __init__(self):
        self._stringio = io.StringIO()

    def __str__(self):
        return self._stringio.getvalue()

    def append(self, *objects, sep=' ', end=''):
        print(*objects, sep=sep, end=end, file=self._stringio)


class Util:
    @staticmethod
    def check_argument():
        pass

    @staticmethod
    def immutable_list(cls):
        pass

    @staticmethod
    def immutable_set(cls):
        pass

    @staticmethod
    def check_not_null(cls, string):
        pass

    @staticmethod
    def immutable_multimap(cls):
        pass

    @staticmethod
    def string_literal_with_double_quotes(value, indent):
        pass
        # StringBuilder result = new StringBuilder(value.length() + 2)
        # result.append('"')
        # for i in range(0, len(value)):
        #     c = value[i]
        #     # trivial case: single quote must not be escaped
        #     if c == '\'':
        #         result.append("'")
        #         continue
        #     # trivial case: double quotes must be escaped
        #     if c == '\"':
        #         result.append("'")
        #         continue
        #     # default case: just let character literal do its work
        #     result.append(character_literal_without_single_quotes(c))
        #     # need to append indent after linefeed?
        #     if c == '\n' and i+1 < len(value):
        #         result.append("\"\n").append(indent).append(indent).append("+ \"")
        # result.append('"')
        # return str(result)

    @staticmethod
    def check_state(condition, format1, *args):
        pass

    @staticmethod
    def character_literal_without_single_quotes(c):
        pass
        if c == '\b':
            return "\\b"
        elif c == '\t':
            return "\\t"
        elif c == '\n':
            return "\\n"
        elif c == '\f':
            return "\\f"
        elif c == '\r':
            return "\\r"
        elif c == '\"':
            return "\""
        elif c == '\'':
            return "\\'"
        elif c == '\\':
            return "\\\\"
        else:
            pass
            # return isISOControl(c) ? String.format("\\u%04x", (int) c): Character.toString(c);
