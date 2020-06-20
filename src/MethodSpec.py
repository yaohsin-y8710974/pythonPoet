from ClassName import ClassName
from CodeBlock import CodeBlock
from ParameterSpec import ParameterSpec
from TypeName import TypeName
from AnnotationSpec import AnnotationSpec
from multipledispatch import dispatch
from Util import Util


class MethodSpec:
    CONSTRUCTOR = "<init>"

    def __init__(self, builder):
        code = builder.code.build()
        self.name = builder.name  # self.name = Util.check_not_null(builder.name, "name == null")
        self.pythondoc = builder.pythondoc.build()
        self.annotations = builder.annotations  # self.annotations = Util.immutable_list(builder.annotations)
        # self.modifiers = Util.immutable_list(builder.modifiers)
        self.type_variables = builder.type_variables  # self.type_variables = Util.immutable_list(builder.type_variables)
        self.return_type = builder.return_type
        self.parameters = builder.parameters  # self.parameters = Util.immutable_list(builder.parameters)
        self.varargs = builder.varargs
        self.exceptions = builder.exceptions  # self.exceptions = Util.immutable_list(builder.exceptions)
        self.default_value = builder.default_value
        self.code = code

    @staticmethod
    def method_builder(method_name):
        builder = Builder(method_name)
        return builder

    def emit(self, code_writer, enclosing_name):
        # code_writer.emit_python_doc(self.pythondoc)  ####################
        code_writer.emit_annotations(self.annotations, False)
        code_writer.emit("def ")
        # code_writer.emit_modifiers(self.modifiers, implicit_modifiers)

        # if not self.type_variables:
        #     code_writer.emit_type_variables(self.type_variables)
        #     code_writer.emit(" ")

        # if self.is_constructor():
        #     code_writer.emit("$L($Z", enclosing_name)
        # else:
        #     code_writer.emit("$T $L($Z", self.return_type, self.name)
        code_writer.emit("$L($Z", self.name)  # code_writer.emit("$T $L($Z", self.return_type, self.name)

        first_parameter = True
        for parameter in self.parameters:
            if not first_parameter:
                code_writer.emit(",").emit_wrapping_space()
            parameter.emit(code_writer, not parameter and self.varargs)
            first_parameter = False

        code_writer.emit(")")

        if self.default_value is not None and not self.default_value:
            code_writer.emit(" default ")
            code_writer.emit(self.default_value)

        if self.exceptions:
            code_writer.emit_wrapping_space().emit("throws")
            first_exception = True
            for exception in self.exceptions:
                if not first_exception:
                    code_writer.emit(",")
                code_writer.emit_wrapping_space().emit("$T", exception)
                first_exception = False

        # if (hasModifier(Modifier.ABSTRACT)) {
        #    codeWriter.emit(";\n");
        # }
        # else if (hasModifier(Modifier.NATIVE)) {
        #    // Code is allowed to support stuff like GWT JSNI.
        #    codeWriter.emit(code);
        #    codeWriter.emit(";\n");
        # }
        # else {
        #    codeWriter.emit(" {\n");
        #    codeWriter.indent();
        #    codeWriter.emit(code);
        #    codeWriter.unindent();
        #    codeWriter.emit("}\n");
        # }

        code_writer.emit(":\n")
        code_writer.indent_()
        code_writer.emit(self.code)
        code_writer.unindent_()
        code_writer.emit("\n")

    # def is_constructor(self):
    #     return self.name.equals(self.CONSTRUCTOR)


class Builder:
    code = CodeBlock.builder()
    pythondoc = CodeBlock.builder()
    annotations = list()
    modifiers = list()
    type_variables = list()
    return_type = TypeName
    parameters = list()
    exceptions = set()
    varargs = bool
    default_value = CodeBlock

    def __init__(self, method_name):
        # checkNotNull(name, "name == null");
        # checkArgument(name.equals(CONSTRUCTOR) | | SourceVersion.isName(name), "not a valid name: %s", name);
        self.name = method_name
        self.annotations = list()
        self.parameters = list()
        self.code = CodeBlock.builder()
        # this.returnType = name.equals(CONSTRUCTOR) ? null: TypeName.VOID;

    @dispatch(AnnotationSpec)
    def add_annotation(self, annotation_spec):
        self.annotations.append(annotation_spec)
        return self

    @dispatch(ClassName)
    def add_annotation(self, annotation):
        self.annotations.append(AnnotationSpec.builder(annotation).build())
        return self

    def add_statement(self, format1, *args):
        self.code.add_statement(format1, args)
        return self

    def add_statement__code_block(self, code_block):
        self.code.add_statement__code_block(code_block)
        return self

    def add_parameter(self, parameter_name):
        return self.add_parameter__code_block(ParameterSpec.builder(parameter_name).build())

    def add_parameter__code_block(self, parameter_spec):
        self.parameters.append(parameter_spec)
        return self

    def add_code(self, format1, *args):
        self.code.add(format1, args)

    def add_code__code_block(self, code_block):
        self.code.add(code_block)

    def begin_control_flow(self, control_flow, *args):
        self.code.begin_control_flow(control_flow, args)
        return self

    def begin_control_flow__code_block(self, code_block):
        return self.begin_control_flow("$L", code_block)

    def next_control_flow(self, control_flow, *args):
        self.code.next_control_flow(control_flow, args)
        return self

    def next_control_flow__code_block(self, code_block):
        return self.next_control_flow("$L", code_block)

    def end_control_flow(self):
        self.code.end_control_flow()
        return self

    def add_comment(self, format1, *args):
        self.code.add("# " + format1 + "\n", args)

    def build(self):
        methodspec = MethodSpec(self)
        return methodspec
