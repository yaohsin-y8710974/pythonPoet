from click._compat import isidentifier
from multipledispatch import dispatch
from CodeBlock import CodeBlock
from LineWrapper import LineWrapper
from TypeSpec import TypeSpec
from AnnotationSpec import AnnotationSpec
from ClassName import ClassName
from TypeName import TypeName
from Util import Util


class CodeWriter:
    trailing_new_line = bool()
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
    importable_types = dict()
    typespec_stack = list()
    static_imports = list()
    static_import_class_names = set()
    referenced_names = set()

    def __init__(self, out, indent, static_imports, imported_types=None):
        if imported_types is None:
            # self.indent = Util.check_not_null(indent, "indent == null")
            # self.static_imports = Util.check_not_null(static_imports, "staticImports == null")
            self.indent = indent
            self.static_imports = static_imports
            self.out = LineWrapper(out, indent, 100)
        else:
            # self.indent = Util.check_not_null(indent, "indent == null")
            # self.imported_types = Util.check_not_null(imported_types, "importedTypes == null")
            # self.static_imports = Util.check_not_null(static_imports, "staticImports == null")
            self.indent = indent
            self.imported_types = imported_types
            self.static_imports = static_imports
            self.out = LineWrapper(out, indent, 100)
        # this.staticImportClassNames = new LinkedHashSet<>();
        # for (String signature : staticImports) {
        #       staticImportClassNames.add(signature.substring(0, signature.lastIndexOf('.')));
        #  }
        for signature in static_imports:
            self.static_import_class_names.add(signature.substring(0, signature.rfind('.')))

    @dispatch()
    def indent_(self):
        return self.indent_(1)

    @dispatch(int)
    def indent_(self, levels):
        self.indent_level += levels
        return self

    @dispatch()
    def unindent_(self):
        return self.unindent_(1)

    @dispatch(int)
    def unindent_(self, levels):
        # Util.check_argument(self.indent_level - levels >= 0, "cannot unindent %s from %s", levels, self.indent_level)
        self.indent_level -= levels
        return self

    def push_package(self, package_name):
        # Util.check_state(self.package_name == self.NO_PACKAGE, "package already set: %s", self.package_name)
        # self.package_name = Util.check_not_null(package_name, "package_name == null")
        self.package_name = package_name
        return self

    def pop_package(self):
        # Util.check_state(self.package_name != self.NO_PACKAGE, "package not set")
        self.package_name = self.NO_PACKAGE
        return self

    def push_type(self, type1):
        self.typespec_stack.append(type1)
        return self

    def pop_type(self):
        self.typespec_stack.pop()
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

    def emit_type_variables(self, type_variables):
        if not type_variables:
            return

        self.emit("<")
        first_type_variable = True
        for type_variable in type_variables:
            if not first_type_variable:
                self.emit(", ")
            self.emit_annotations(type_variable.annotations, True)
            self.emit("$L", type_variable.name)
            first_bound = True
            for bound in type_variable.bounds:
                if first_bound is True:
                    self.emit("extends $T", bound)
                else:
                    self.emit(" & $T", bound)
                first_bound = False
            first_type_variable = False
        self.emit(">")

    @dispatch(str, str)
    def emit(self, format1, *args):
        args = str(args).strip("',()")  # eliminate special symbol
        return self.emit(CodeBlock.of(format1, args))

    @dispatch(str)
    def emit(self, s):
        return self.emit_and_indent(s)

    @dispatch(CodeBlock)
    def emit(self, code_block):
        return self.emit(code_block, False)

    @dispatch(CodeBlock, bool)
    def emit(self, code_block, ensure_trailing_new_line):
        a = 0
        deferred_type_name = None  # used by "import static" logic
        for part in code_block.format_parts:
            # print('part = ', part)
            if part == "$L":
                self.emit_literal(code_block.args[a])
                a += 1
            elif part == "$N":
                self.emit_and_indent(code_block.args[a])
                a += 1
            elif part == "$S":
                string = str(code_block.args[a])
                a += 1
                # Emit null as a literal null: no quotes.
                if string:
                    self.emit_and_indent(
                        Util.string_literal_with_double_quotes(string, self.indent))  # Util not finish yet
                else:
                    self.emit_and_indent("None")
            elif part == "$T":
                type_name = TypeName(code_block.args[a], None)
                # defer "type_name.emit(self)" if next format part will be handled by the default case
                if isinstance(type_name, ClassName) and part:
                    if not code_block.format_parts[part.startwith('$')]:
                        candidate = type_name
                        if candidate.canonical_name in self.static_import_class_names:
                            # checkState(deferredTypeName == null, "pending type for static import?!");
                            if not deferred_type_name:
                                deferred_type_name = candidate
                # type_name.emit(self)
            elif part == "$$":
                self.emit_and_indent("$")
            elif part == "$>":
                self.indent_()
            elif part == "$<":
                self.unindent_()
            elif part == "$[":
                # Util.check_state(self.statement_line != -1, "statement enter $[ followed by statement enter $[")
                self.statement_line = 0
            elif part == "$]":
                # Util.check_state(self.statement_line != -1, "statement enter $[ followed by statement enter $[")
                if self.statement_line > 0:
                    self.unindent_(2)  # End a multi-line statement. Decrease the indentation level.
                self.statement_line = -1
            elif part == "$W":
                self.out.wrapping_space(self.indent_level + 2)
            elif part == "$Z":
                self.out.zero_width_space(self.indent_level + 2)
            else:
                # handle deferred type
                if deferred_type_name:
                    if part.startswith("."):
                        if self.emit_static_import_member(ClassName.canonical_name, part):
                            # okay, static import hit and all was emitted, so clean-up and jump to next part
                            deferred_type_name = None
                    deferred_type_name.emit(self)
                    deferred_type_name = None
                self.emit_and_indent(part)
        if ensure_trailing_new_line and self.out.last_char() != '\n':
            self.emit("\n")
        return self

    def emit_wrapping_space(self):
        # self.out.wrapping_space(self.indent_level + 2)   ##########
        return self

    def emit_static_import_member(self, canonical, part):
        part_without_leading_dot = part[1:]
        if part_without_leading_dot:
            return False
        first = part_without_leading_dot[0]
        if not isidentifier(first):
            return False
        explicit = canonical + "." + self.extract_member_name(part_without_leading_dot)
        wildcard = canonical + ".*"
        if explicit in self.static_imports or wildcard in self.static_imports:
            self.emit_and_indent(part_without_leading_dot)
            return True
        return False

    def emit_literal(self, o):
        if isinstance(o, TypeSpec):
            # typespec = TypeSpec
            # typespec.emit(self, None)
            o.emit(self, None)
        elif isinstance(o, AnnotationSpec):
            # annotationspec = AnnotationSpec
            # annotationspec.emit(self, True)
            o.emit(self, True)
        elif isinstance(o, CodeBlock):
            # codeblock = CodeBlock
            # self.emit(codeblock)
            self.emit(o)
        else:
            self.emit_and_indent(str(o))

    def emit_and_indent(self, s):
        first = True
        # count = 0
        # print('=======================')
        # print('s = ', s)
        # for line in s.split(r'\\R', -1):
        for line in s.split('\n'):
            # count += 1
            # print('line = ', line)
            # print('count = ', count)
            # Emit a newline character. Make sure blank lines in Pythondoc & comments look good.
            if not first:
                if (self.pythondoc or self.comment) and self.trailing_new_line:
                    self.emit_indentation()
                    if self.pythondoc:
                        self.out.append(" *")
                    else:
                        self.out.append("#")
                self.out.append("\n")
                self.trailing_new_line = True
                if self.statement_line != -1:
                    if self.statement_line == 0:
                        self.indent_(2)
                    self.statement_line += 1
            first = False
            if not line:
                continue  # Don't indent empty lines.
            # Emit indentation and comment prefix if necessary
            if self.trailing_new_line:
                self.emit_indentation()
                if self.pythondoc:
                    self.out.append(" * ")
                elif self.comment:
                    self.out.append("# generated by PythonPoet")
            self.out.append(line)
            self.trailing_new_line = False
        return self

    def emit_indentation(self):
        for i in range(self.indent_level):
            self.out.append(self.indent)

    # Returns the types that should have been imported for this code. If there were any simple name collisions,
    # that type's first use is imported.
    def suggested_imports(self):
        result = self.importable_types
        for key in self.referenced_names:
            if key in result:
                del result[key]
        return result
        # Map < String, ClassName > result = new LinkedHashMap <> (importableTypes);
        # result.keySet().removeAll(referencedNames);
        # return result;

    def emit_annotations(self, annotations, inline):
        for annotationspec in annotations:
            annotationspec.emit(self, inline)
            if inline is True:
                self.emit(" ")
            else:
                self.emit("\n")

    @staticmethod
    def extract_member_name(part):
        # Util.check_argument()
        for i in range(1, len(part)):
            if not isidentifier(part[0:i]):
                return part[0:i]
        return part

    def lookup_name(self, class_name):
        # Find the shortest suffix of className that resolves to className. This uses both local type
        # names (so 'Entry' in 'Map' refers to 'Map.Entry'). Also uses imports.
        name_resolved = False
        # for (ClassName c = className; c != null; c = c.enclosingClassName()) {
        #     ClassName resolved = resolve(c.simpleName());
        #     nameResolved = resolved != null;
        #
        #     if (resolved != null & & Objects.equals(resolved.canonicalName, c.canonicalName)) {
        #         int suffixOffset = c.simpleNames().size() - 1;
        #         return join(".", className.simpleNames().subList(
        #             suffixOffset, className.simpleNames().size()));
        #     }
        # }
        #
        # If the name resolved but wasn't a match, we're stuck with the fully qualified name.
        if name_resolved:
            return class_name.canonical_name

        # If the case is in the same package, we're done.
        # if (Objects.equals(packageName, className.packageName())) {
        #     referencedNames.add(className.topLevelClassName().simpleName());
        #     return join(".", className.simpleNames());

        # We'll have to use the fully-qualified name. Mark the type as importable for a future pass.
        if not self.pythondoc:
            self.importable_type(class_name)

        return class_name.canonical_name

    def importable_type(self, class_name):
        if class_name.package_name():
            return
        toplevel_class_name = class_name.top_level_class_name()
        simple_name = toplevel_class_name.simple_name()
        replaced = self.importable_types.update({simple_name: toplevel_class_name})
        if replaced:
            self.importable_types.update({simple_name: replaced})  # On collision, prefer the first inserted.

    def imported_types_(self):
        return self.imported_types
