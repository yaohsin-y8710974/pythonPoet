from CodeBlock import CodeBlock
from TypeName import TypeName
from Util import Util


class TypeSpec:
    def __init__(self, builder):
        self.pythondoc = builder.pythondoc.build()
        self.annotations = Util.immutable_list(builder.annotations)
        self.anonymous_type_arguments = builder.anonymous_type_arguments
        self.field_specs = Util.immutable_list(builder.field_specs)
        self.method_specs = Util.immutable_list(builder.method_specs)
        self.type_specs = Util.immutable_list(builder.type_specs)
        self.superinterfaces = Util.immutable_list(builder.superinterfaces)
        self.superclass = builder.superinterfaces

    @staticmethod
    def class_builder(class_name):
        builder = Builder(class_name)
        return builder

    def emit(self, code_writer, enum_name):
        # previous_statement_line = code_writer.statement_line
        # code_writer.statement_line = -1
        # try:
        #     if enum_name is not None:
        #         code_writer.emit_python_doc(self.pythondoc)
        #         code_writer.emit_annotations(self.annotations, False)
        #         code_writer.emit("$L", enum_name)
        #         if self.anonymous_type_arguments.format_parts.is_empty():
        #             code_writer.emit("(")
        #             code_writer.emit(self.anonymous_type_arguments)
        #             code_writer.emit(")")
        #         if self.field_specs.is_empty() and self.method_specs.is_empty() and self.type_specs.is_empty():
        #             return  # Avoid unnecessary braces "{}".
        #         code_writer.emit(" {\n")
        #     elif self.anonymous_type_arguments is not None:
        #         supertype = not (self.superinterfaces and self.superinterfaces.get(0) or self.superclass)
        #         code_writer.emit("new $T(", supertype)
        #         code_writer.emit(self.anonymous_type_arguments)
        #         code_writer.emit(") {\n")
        #     else:
        #         print()
        # finally:
        #     code_writer.statement_line = previous_statement_line
        print()

class Builder:
    pythondoc = CodeBlock.builder()
    annotations = list()
    anonymous_type_arguments = CodeBlock
    type_specs = list()
    method_specs = list()
    field_specs = list()
    superclass = TypeName
    superinterfaces = list()

    def __init__(self, class_name):
        print()

    def build(self):
        typespec = TypeSpec(self)
        return typespec

    def add_method(self, method_spec):
        return self
