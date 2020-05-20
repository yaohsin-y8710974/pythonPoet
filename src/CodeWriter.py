from multipledispatch import dispatch
from CodeBlock import CodeBlock
from LineWrapper import LineWrapper
from TypeName import TypeName
from ClassName import ClassName
from Util import Util


class CodeWriter:
    trailing_new_line = bool
    NO_PACKAGE = str()
    pythondoc = False
    comment = False
    out = LineWrapper
    # when emitting a statement, this is the line of the statement currently being written. The first
    # line of a statement is indented normally and subsequent wrapped lines are double-indented. This
    # is -1 when the currently-written line isn't part of a statement.
    statement_line = -1
    indent_level = int()
    package_name = NO_PACKAGE
    imported_types = dict()
    typespec_stack = list()
    static_imports = list()

    def __init__(self, out, indent, static_imports, imported_types=None):
        if imported_types is None:
            self.out = LineWrapper(out, indent, 100)
            self.indent = Util.check_not_null(indent, "indent == null")
            # self.imported_types = Util.check_not_null(imported_types, "importedTypes == null")
            self.static_imports = Util.check_not_null(static_imports, "staticImports == null")
        else:
            self.out = LineWrapper(out, indent, 100)
            self.indent = Util.check_not_null(indent, "indent == null")
            self.imported_types = Util.check_not_null(imported_types, "importedTypes == null")
            self.static_imports = Util.check_not_null(static_imports, "staticImports == null")
        # this.staticImportClassNames = new LinkedHashSet<>();
        # for (String signature : staticImports) {
        #       staticImportClassNames.add(signature.substring(0, signature.lastIndexOf('.')));
        #  }

    # def imported_types(self):
    #     return self.imported_types

    @dispatch()
    def indent(self):
        return self.indent(1)

    @dispatch(int)
    def indent(self, levels):
        self.indent_level = self.indent_level + levels
        return self

    @dispatch()
    def unindent(self):
        return self.unindent(1)

    @dispatch(int)
    def unindent(self, levels):
        # Util.check_argument(self.indent_level - levels >= 0, "cannot unindent %s from %s", levels, self.indent_level)
        self.indent_level -= levels
        return self

    def push_package(self, package_name):
        Util.check_state(self.package_name == self.NO_PACKAGE, "package already set: %s", self.package_name)
        self.package_name = Util.check_not_null(package_name, "package_name == null")
        return self

    def pop_package(self):
        Util.check_state(self.package_name != self.NO_PACKAGE, "package not set")
        self.package_name = self.NO_PACKAGE
        return self

    def push_type(self, type):
        self.typespec_stack.append(type)
        return self

    def pop_type(self):
        # self.typespec_stack.pop()
        return self

    def emit_comment(self, code_block):
        self.trailing_new_line = True
        self.comment = True
        try:
            self.emit(code_block)
            self.emit("\n")
        finally:
            self.comment = False

    def emit_python_doc(self, pythondoc_codeblock):
        if not pythondoc_codeblock:
            return
        self.emit("/**\n")
        self.pythondoc = True
        try:
            self.emit(pythondoc_codeblock)
        finally:
            self.pythondoc = False
        self.emit(" */\n")

    def emit_annotation(self, annotations, in_line):
        for annotation_spec in annotations:
            annotation_spec.emit(self, in_line)
            if in_line is True:
                self.emit(" ")
            else:
                self.emit("\n")

    # def emit_modifiers(self):
    #     print()

    def emit_type_variables(self, type_variables):
        print()
        # if not type_variables:
        #     return
        #
        # self.emit("<")
        # first_type_variable = True
        # for type_variable in type_variables:
        #     if not first_type_variable:
        #         self.emit(", ")
        #     self.emit_annotations(type_variable.annotations, True)
        #     self.emit("$L", type_variable.name)
        #     first_bound = True
        #     for bound in type_variable.bounds:
        #         if first_bound is True:
        #             self.emit("extends $T", bound)
        #         else:
        #             self.emit(" & $T", bound)
        #         first_bound = False
        #     first_type_variable = False
        # self.emit(">")

    @dispatch(str, list)
    def emit(self, format, *args):
        print()
        return self.emit(CodeBlock.of(format, args))

    @dispatch(str)
    def emit(self, s: str):
        return self.emit_and_indent(s)

    @dispatch(CodeBlock)
    def emit(self, code_block):
        a = 0
        # deferred_type_name = ClassName
        deferred_type_name = None  # used by "import static" logic
        part_iterator = iter(code_block.format_parts)
        while part_iterator.__next__():
            part = next(part_iterator)
            if part == "$L":
                self.emit_literal(code_block.args.get(a + 1))
            elif part == "$N":
                self.emit_and_indent(code_block.args.get(a + 1))
            elif part == "$S":
                string = str(code_block.args.get(a + 1))
                # self.emit_and_indent()
            elif part == "$T":
                type_name = TypeName(code_block.args.get(a + 1))
                # defer "type_name.emit(self)" if next format part will be handled by the default case

            elif part == "$$":
                self.emit_and_indent("$")
            elif part == "$>":
                self.indent()
            elif part == "$<":
                self.unindent()
            elif part == "$[":
                Util.check_state(self.statement_line != -1, "statement enter $[ followed by statement enter $[")
                self.statement_line = 0
            elif part == "$]":
                Util.check_state(self.statement_line != -1, "statement enter $[ followed by statement enter $[")
                if self.statement_line > 0:
                    self.unindent(2)  # End a multi-line statement. Decrease the indentation level.
            elif part == "$W":
                self.out.wrapping_space(self.indent_level + 2)
            elif part == "$Z":
                self.out.zero_width_space(self.indent_level + 2)
            else:
                # handle deferred type
                if deferred_type_name is not None:
                    if part.startswith("."):
                        if self.emit_static_import_member(ClassName.canonical_name, part):
                            deferred_type_name = None
                            break
                    deferred_type_name.emit(self)
                    deferred_type_name = None
                self.emit_and_indent(part)
                break
        return self

    def emit_wrapping_space(self):
        self.out.wrapping_space(self.indent_level + 2)
        return self

    def emit_static_import_member(self):
        print()

    def emit_literal(self):
        print()

    def emit_and_indent(self, s):
        first = True
        for line in s.split("\n", -1):
            if not first:
                if (self.pythondoc or self.comment) and self.trailing_new_line:
                    self.emit_indentation()
                    if self.pythondoc:  # self.out.append(self.pythondoc ? " *" : "//")
                        self.out.append(" *")
                    else:
                        self.out.append(" //")
                self.out.append("\n")
                self.trailing_new_line = True
                if self.statement_line != -1:
                    if self.statement_line == 0:
                        self.indent(2)
                    self.statement_line += 1
            first = False
            if line:
                continue  # Don't indent empty lines.

            # Emit indentation and comment prefix if necessary
            if self.trailing_new_line:
                self.emit_indentation()
                if self.pythondoc:
                    self.out.append(" * ")
                elif self.comment:
                    self.out.append("// ")
            self.out.append(line)
            self.trailing_new_line = False
        return self

    def emit_indentation(self):
        for i in range(self.indent_level):
            self.out.append(self.indent)

    def suggested_imports(self):
        print()

    def emit_annotations(self, annotations, inline):
        for annotationspec in annotations:
            annotationspec.emit(self, inline)
            if inline is True:
                self.emit(" ")
            else:
                self.emit("\n")
