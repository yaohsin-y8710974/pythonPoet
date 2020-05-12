from CodeBlock import CodeBlock
from CodeWriter import CodeWriter
from TypeSpec import TypeSpec
from Util import Util
from typing import overload

class PythonFile:
    # file_comment = CodeBlock
    # package_name = ""
    # type_spec = TypeSpec
    # skip_python_imports = bool
    # static_imports = set()
    # indent = ""

    NULL_APPENDABLE = None

    def __init__(self, builder):
        print()
        self.file_comment = builder.file_comment.build()
        self.package_name = builder.package_name
        self.type_spec = builder.type_spec
        self.skip_python_imports = builder.skip_python_imports
        self.static_imports = builder.static_imports  # self.static_imports = Util.immutable_set(builder.static_imports)
        self.indent = builder.indent

    def builder(package_name, type_spec):
        Util.check_not_null(package_name, "package_name == null")
        Util.check_not_null(type_spec, "type_spec == null")
        builder = Builder(package_name, type_spec)
        return builder

    def write_to(self, out):
        import_collector = CodeWriter(PythonFile.NULL_APPENDABLE, self.indent, self.static_imports)
        self.emit(import_collector)
        suggest_imports = import_collector.suggested_imports()
        code_writer = CodeWriter(out, self.indent, suggest_imports, self.static_imports)
        self.emit(code_writer)

    def emit(self, code_writer):
        code_writer.push_package(self.package_name)
        if not(self.file_comment.is_empty()):
            code_writer.emit_comment(self.file_comment)
        if not self.package_name:
            code_writer.emit("package $L\n", self.package_name)
            code_writer.emit("\n")
        if not self.static_imports:
            for signature in self.static_imports:
                code_writer.emit("import static $L\n", signature)
            code_writer.emit("\n")
        #
        imported_types_count = 0
        # for class_name in code_writer.imported_types():
        #     if self.skip_python_imports and class_name.package_name().equals(""):
        #         continue
        #     code_writer.emit("import $L\n", class_name.without_annotations())
        #     imported_types_count += 1
        #
        if imported_types_count > 0:
            code_writer.emit("\n")

        self.type_spec.emit(code_writer, None)  # java code: typeSpec.emit(codeWriter, null, Collections.emptySet())
        code_writer.pop_package()


class Builder:
    package_name = ''
    type_spec = TypeSpec
    file_comment = CodeBlock.builder()
    static_imports = set()
    skip_python_imports = bool
    indent = "  "

    def __init__(self, package_name, type_spec):
        self.package_name = package_name
        self.type_spec = type_spec

    def build(self):
        python_file = PythonFile(self)
        return python_file
