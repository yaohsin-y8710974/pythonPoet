from CodeBlock import CodeBlock
from TypeName import TypeName
from Util import Util


class MethodSpec:
    def __init__(self, builder):
        code = builder.code.build()
        # check_argument(abstract method cannot have code)
        # check_argument(last parameter of varargs method must be an array)
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
        # Util.check_not_null(method_name, "name == null")
        # Util.check_argument("if method is CONSTRUCTOR")
        self.name = method_name
        # self.return_type = method_name.equals(CONSTRUCTOR)

    def add_annotation(self, annotation_spec):
        self.annotations.append(annotation_spec)
        return self

    def add_statement(self, code_block):
        self.code.add_statement(code_block)

    def build(self):  # done
        methodspec = MethodSpec(self)
        return methodspec
