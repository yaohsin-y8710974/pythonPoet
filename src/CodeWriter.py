from LineWrapper import LineWrapper


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

    def emit_python_doc(self):
        print()

    def emit_annotation(self):
        print()

    def emit_modifiers(self):
        print()

    def emit_type_variables(self):
        print()

    def emit(self, code_block):
        print()

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

    def emit_and_indent(self):
        print()

    def emit_indentation(self):
        print()

    def suggested_imports(self):
        print()
