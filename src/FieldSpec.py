from CodeBlock import CodeBlock
from TypeName import TypeName
from multipledispatch import dispatch


class FieldSpec:
    type1 = TypeName
    name = str()
    pythondoc = CodeBlock
    annotations = list()
    initializer = CodeBlock

    def __init__(self, builder):
        self.type1 = builder.type1
        self.name = builder.name
        self.pythondoc = builder.pythondoc.build()
        self.annotations = builder.annotations
        # self.modifiers = Util.immutable_set(builder.modifiers)
        if builder.initializer is None:
            self.initializer = CodeBlock.builder().build()
        else:
            self.initializer = builder.initializer

    def emit(self, code_writer):
        code_writer.emit_python_doc(self.pythondoc)
        code_writer.emit_annotations(self.annotations, False)
        # codeWriter.emitModifiers(modifiers, implicitModifiers);
        code_writer.emit("$T $L", self.type1, self.name)
        if self.initializer:
            code_writer.emit(" = ")
            code_writer.emit(self.initializer)
        code_writer.emit(";\n")

    @staticmethod
    def builder(type1, name):
        builder = Builder(type1, name)
        return builder


class Builder:
    type1 = TypeName
    name = str()

    pythondoc = CodeBlock.builder()
    annotations = list()
    initializer = None

    def __init__(self, type1, name):
        self.type1 = type1
        self.name = name

    @dispatch(str, str)
    def add_python_doc(self, format1, *args):
        self.pythondoc.add(format1, args)
        return self

    @dispatch(CodeBlock)
    def add_python_doc(self, block):
        self.pythondoc.add(block)
        return self

    def build(self):
        fieldspec = FieldSpec(self)
        return fieldspec