from CodeBlock import CodeBlock
from CodeWriter import CodeWriter
from TypeSpec import TypeSpec
from ClassName import ClassName
from Util import Util


class PythonFile:
    file_comment = CodeBlock
    package_name = str()
    type_spec = TypeSpec
    skip_python_imports = bool()
    static_imports = set()
    indent = str()

    def __init__(self, builder):
        self.file_comment = builder.file_comment.build()
        self.package_name = builder.package_name
        self.type_spec = builder.type_spec
        self.skip_python_imports = builder.skip_python_imports
        self.static_imports = builder.static_imports  # self.static_imports = Util.immutable_set(builder.static_imports)
        self.indent = builder.indent

    @staticmethod
    def builder(package_name, type_spec):
        # Util.check_not_null(package_name, "package_name == null")
        # Util.check_not_null(type_spec, "type_spec == null")
        builder = Builder(package_name, type_spec)
        return builder

    def write_to(self, writer):
        # First pass: emit the entire class, just to collect the types we'll need to import.
        import_collector = CodeWriter(writer, self.indent, self.static_imports, None)
        self.emit(import_collector)
        # suggested_imports = import_collector.suggested_imports()
        # Second pass: write the code, taking advantage of the imports.
        # code_writer = CodeWriter(writer, self.indent, self.static_imports, suggested_imports)
        # self.emit(code_writer)

    def emit(self, code_writer):
        code_writer.push_package(self.package_name)

        # if self.file_comment:  #############
        #     code_writer.emit_comment(self.file_comment)  ############

        if self.package_name:
            code_writer.emit("from $L import $L\n", self.package_name)
            code_writer.emit("\n")

        if self.static_imports:
            for signature in self.static_imports:
                code_writer.emit("import static $L\n", signature)
            code_writer.emit("\n")

        imported_types_count = 0
        for class_name in code_writer.imported_types.values():
            # if (skipJavaLangImports && className.packageName().equals("java.lang")
            #                         && !alwaysQualify.contains(className.simpleName))
            if self.skip_python_imports:
                continue
            code_writer.emit("import $L\n", class_name.without_annotations())
            imported_types_count += 1

        if imported_types_count > 0:
            code_writer.emit("\n")

        if self.type_spec:
            self.type_spec.emit(code_writer, None)  # typeSpec.emit(codeWriter, null, Collections.emptySet())
        else:
            TypeSpec.emit_methods(code_writer)  # emit method if TypeSpec is None.
        code_writer.pop_package()


class Builder:
    package_name = str()
    type_spec = TypeSpec
    file_comment = CodeBlock.builder()
    static_imports = set()
    skip_python_imports = bool()
    indent = "    "

    def __init__(self, package_name, type_spec):
        self.package_name = package_name
        self.type_spec = type_spec

    def indent_(self, indent):
        self.indent = indent
        return self

    def skip_python_imports_(self, skip_python_imports):
        self.skip_python_imports = skip_python_imports
        return self

    def add_file_comment(self, format1, *args):
        self.file_comment.add(format1, args)
        return self

    def build(self):
        python_file = PythonFile(self)
        return python_file
