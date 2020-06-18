from multipledispatch import dispatch

from ParameterSpec import ParameterSpec
from Util import Util


class CodeBlock:
    def __init__(self, builder):
        self.format_parts = builder.format_parts  # self.format_parts = Util.immutable_list(builder.format_parts)
        self.args = builder.args  # self.args = Util.immutable_list(builder.args)

    @staticmethod
    def builder():
        builder = Builder()
        return builder

    def add_url(self, url):
        builder = Builder().url(url).build()
        return builder

    def is_empty(self):
        return not self.format_parts

    @staticmethod
    def of(format1, args):
        builder = Builder()
        return builder.add(format1, args).build()


class Builder:
    format_parts = list()
    args = list()

    def __init__(self):
        self.format_parts = list()
        self.args = list()

    def url(self, url):
        self.args.append(url)
        return self

    # Add code with positional or relative arguments.
    #
    # <p>Relative arguments map 1:1 with the placeholders in the format string.
    #
    # <p>Positional arguments use an index after the placeholder to identify which argument index
    # to use. For example, for a literal to reference the 3rd arguments: "$3L" (1 based index)
    #
    # <p>Mixing relative and positional arguments in a call to add is invalid and will result in an error.
    def add(self, format1, *args):
        # has_relative = False
        has_indexed = False
        relative_parameter_count = 0
        indexed_parameter_count = []

        p = 0
        while p < len(format1):
            if format1[p] != '$':
                try:
                    nextp = format1.index('$', p + 1)
                except ValueError:
                    nextp = len(format1)
                self.format_parts.append(format1[p:nextp])
                p = nextp
                continue

            p += 1

            # Consume zero or more digits, leaving 'c' as the first non-digit char after the '$'.
            index_start = p
            while True:
                if p < len(format1):
                    c = format1[p]
                    p += 1
                    if not ('0' <= c <= '9'):
                        break
            index_end = p - 1

            # If 'c' doesn't take an argument, we're done.
            if self.is_no_arg_placeholder(c):
                # Util.check_argument()
                self.format_parts.append("$" + c)
                continue

            # Find either the indexed argument, or the relative argument. (0-based).
            index = int()
            if index_start < index_end:
                index = int(format1[index_start:index_end - 1])
                has_indexed = True
                if len(args) > 0:
                    indexed_parameter_count[index % len(args)] += 1  # modulo is needed, checked below anyway
                else:
                    index = relative_parameter_count
                    has_relative = True
                    relative_parameter_count += 1

            # Util.check_argument()
            # Util.check_argument()
            self.add_argument(format1, c, args[index])

            self.format_parts.append("$" + c)

            # if has_relative:
            #     Util.check_argument()

        # if has_indexed:
        #     unused = list()
        #     for i in range(0, len(args)):
        #         if indexed_parameter_count[i] == 0:
        #             unused.append("$" + str(i + 1))
        #         if len(unused) == 1:
        #             s = ""
        #         else:
        #             s = "s"
        #         # Util.check_argument()

        return self

    def is_no_arg_placeholder(self, c):
        return c == '$' or c == '>' or c == '<' or c == '[' or c == ']' or c == 'W' or c == 'Z'

    def add_argument(self, format1, c, arg):
        if c == 'N':
            self.args.append(self.arg_to_name(arg))
        if c == 'L':
            self.args.append(self.arg_to_literal(arg))
        if c == 'S':
            self.args.append(self.arg_to_string(arg))
        if c == 'T':
            self.args.append(self.arg_to_type(arg))

    def arg_to_name(self, o):
        # if (o instanceof CharSequence)
        #   return o.toString();
        if isinstance(o, ParameterSpec):
            return o.name
        if isinstance(o, FieldSpec):
            return o.name
        if isinstance(o, MethodSpec):
            return o.name
        if isinstance(o, TypeSpec):
            return o.name
        raise Exception('expected name but was ' + o)

    def arg_to_literal(self, o):
        return o

    def arg_to_string(self, o):
        if o is not None:
            return str(o)
        else:
            return None

    def arg_to_type(self, o):
        pass
        # if (o instanceof TypeName) return (TypeName) o;
        # if (o instanceof TypeMirror) return TypeName.get((TypeMirror) o);
        # if (o instanceof Element) return TypeName.get(((Element) o).asType());
        # if (o instanceof Type) return TypeName.get((Type) o);
        # raise Exception('expected type but was ' + o)

    def begin_control_flow(self, control_flow, *args):
        self.add(control_flow + ":\n", args)
        self.indent()
        return self

    def next_control_flow(self, control_flow, *args):
        self.unindent()
        self.add(" }" + control_flow + " {\n", args)
        self.indent()
        return self

    def end_control_flow(self):
        self.unindent()
        # self.add("\n")
        return self

    def add_statement(self, format1, *args):
        self.add("$[")
        self.add(format1, args)
        self.add("\n$]")
        return self

    def add_statement__code_block(self, code_block):
        return self.add_statement("$L", code_block)

    # @dispatch(CodeBlock)
    # def add(self, code_block):
    #     self.format_parts.extend(code_block.format_parts)
    #     self.args.extend(code_block.args)
    #     return self

    def indent(self):
        self.format_parts.append("$>")
        return self

    def unindent(self):
        self.format_parts.append("$<")
        return self

    def clear(self):
        self.format_parts.clear()
        self.args.clear()
        return self

    def build(self):
        codeblock = CodeBlock(self)
        return codeblock


class CodeBlockJoiner:
    delimiter = str()
    builder = Builder()
    first = True

    def __init__(self, delimiter, builder):
        self.delimiter = delimiter
        self.builder = builder

    def add(self, code_block):
        if not self.first:
            self.builder.add(self.delimiter)
        self.first = False

        self.builder.add(code_block)
        return self

    def merge(self, other):
        other_block = other.builder.build()
        if other_block:
            self.add(other_block)
        return self

    def join(self):
        return self.builder.build()
