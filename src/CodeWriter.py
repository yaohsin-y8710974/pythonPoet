from typing import overload

from CodeBlock import CodeBlock
from multipledispatch import dispatch


class CodeWriter:
    trailing_new_line = bool
    # when emitting a statement, this is the line of the statement currently being written. The first
    # line of a statement is indented normally and subsequent wrapped lines are double-indented. This
    # is -1 when the currently-written line isn't part of a statement.

    statement_line = -1

    def __init__(self, out, indent, static_imports, suggested_imports=None):
        print()

    def imported_types(self):
        print()
        return self.imported_types

    def indent(self):
        print()

    def unindent(self):
        print()

    def push_package(self, package_name):
        print()
        # check_state()
        # self.package_name = check_not_null(package_name, "package_name == null")
        # return self

    def pop_package(self):
        print()

    def push_type(self):
        print()

    def pop_type(self):
        print()

    def emit_comment(self, code_block):
        trailing_new_line = True
        comment = True
        try:
            self.emit(code_block)
            self.emit("\n")
        finally:
            comment = False

    def emit_python_doc(self, pythondoc):
        print()

    def emit_annotation(self, annotations, in_line):
        print()

    def emit_modifiers(self):
        print()

    def emit_type_variables(self):
        print()

    @dispatch(str, list)
    def emit(self, format, args):
        print()
        return self.emit(CodeBlock.of(format, args))

    @dispatch(str)
    def emit(self, s: str):
        return self.emit_and_indent(s)

    @dispatch(CodeBlock)
    def emit(self, code_block):
        a = 0
        deferred_type_name = None  # used by "import static" logic
        part_iterator = iter(code_block.format_parts)
        while part_iterator.__next__():
            part = next(part_iterator)
            if part == "$L":
                print()
            elif part == "$N":
                print()
        return self

    def emit_wrapping_space(self):
        print()

    def extract_member_name(self):
        print()

    def emit_static_import_member(self):
        print()

    def emit_literal(self):
        print()

    def lookup_name(self):
        print()

    def importable_type(self):
        print()

    def resolve(self):
        print()

    def stack_class_name(self):
        print()

    def emit_and_indent(self, s):
        print()
        return self

    def emit_indentation(self):
        print()

    def suggested_imports(self):
        print()
