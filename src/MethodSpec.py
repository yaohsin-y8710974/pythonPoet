from CodeBlock import CodeBlock
from TypeName import TypeName
from Util import Util


class MethodSpec:
    CONSTRUCTOR = "<init>"

    def __init__(self, builder):
        code = builder.code.build()
        # checkArgument(code.isEmpty() | | !builder.modifiers.contains(Modifier.ABSTRACT), "abstract method %s cannot have code", builder.name);
        # checkArgument(!builder.varargs | | lastParameterIsArray(builder.parameters), "last parameter of varargs method %s must be an array", builder.name);
        self.name = Util.check_not_null(builder.name, "name == null")
        self.pythondoc = builder.pythondoc.build()
        self.annotations = Util.immutable_list(builder.annotations)
        self.modifiers = Util.immutable_list(builder.modifiers)
        self.type_variables = Util.immutable_list(builder.type_variables)
        self.return_type = builder.return_type
        self.parameters = Util.immutable_list(builder.parameters)
        self.varargs = builder.varargs
        self.exceptions = Util.immutable_list(builder.exceptions)
        self.default_value = builder.default_value
        self.code = code

    def method_builder(method_name):  # done
        builder = Builder(method_name)
        return builder

    def emit(self, code_writer, enclosing_name, implicit_modifiers):
        code_writer.emit_python_doc(self.pythondoc)
        code_writer.emit_annotations(self.annotations, False)
        code_writer.emit_modifiers(self.modifiers, implicit_modifiers)

        if not self.type_variables:
            code_writer.emit_type_variables(self.type_variables)
            code_writer.emit(" ")

        if self.is_constructor():
            code_writer.emit("$L($Z", enclosing_name)
        else:
            code_writer.emit("$T $L($Z", self.return_type, self.name)

        first_parameter = True
        for i in iter(self.parameters):
            if i.__next__:
                parameter = next(i)
                if not first_parameter:
                    code_writer.emit(",").emit_wrapping_space()
                parameter.emit(code_writer, not i.__next__() and self.varargs)
                first_parameter = False

        code_writer.emit(")")

        if self.default_value is not None and not self.default_value:
            code_writer.emit(" default ")
            code_writer.emit(self.default_value)

        if not self.exceptions:
            code_writer.emit_wrapping_space_("throws")
            first_exception = True
            for exception in self.exceptions:
                if not first_exception:
                    code_writer.emit(",")
                code_writer.emit_wrapping_space().emit("$T", exception)
                first_exception = False
        """
         if (hasModifier(Modifier.ABSTRACT)) {
            codeWriter.emit(";\n");
         } 
         else if (hasModifier(Modifier.NATIVE)) {
            // Code is allowed to support stuff like GWT JSNI.
            codeWriter.emit(code);
            codeWriter.emit(";\n");
         } 
         else {
            codeWriter.emit(" {\n");
            codeWriter.indent();
            codeWriter.emit(code);
            codeWriter.unindent();
            codeWriter.emit("}\n");
         }
        """

    def is_constructor(self):
        return self.name.equals(self.CONSTRUCTOR)


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

    def __init__(self, method_name):  # done
        # checkNotNull(name, "name == null");
        # checkArgument(name.equals(CONSTRUCTOR) | | SourceVersion.isName(name), "not a valid name: %s", name);
        self.name = method_name
        # this.returnType = name.equals(CONSTRUCTOR) ? null: TypeName.VOID;

    def add_annotation(self, annotation_spec):
        self.annotations.append(annotation_spec)
        return self

    def add_statement(self, code_block):
        self.code.add_statement(code_block)

    def build(self):  # done
        methodspec = MethodSpec(self)
        return methodspec
