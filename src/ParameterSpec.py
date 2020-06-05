from TypeName import TypeName
from Util import Util


class ParameterSpec:
    name = ""
    annotations = list()
    modifiers = set()
    type1 = TypeName

    def __init__(self, builder):
        self.name = builder.name
        self.annotations = builder.annotations  # self.annotations = Util.immutable_list(builder.annotations)
        # self.modifiers = Util.immutable_set(builder.modifiers)
        # self.type1 = Util.check_not_null(builder.type1, "type == null")

    def emit(self, code_writer, varargs):
        code_writer.emit_annotations(self.annotations, True)
        # no need to handle parameter type in python.
        # if varargs:
        #     TypeName.as_array(self.type1).emit(code_writer, True)
        # else:
        #     self.type1.emit(code_writer)
        code_writer.emit(" $L", self.name)

    @staticmethod
    def builder(parameter_name):
        builder = Builder(parameter_name)
        return builder


class Builder:
    type1 = TypeName
    name = str()
    annotations = list()

    def __init__(self, name):
        self.name = name

    def build(self):
        parameterspec = ParameterSpec(self)
        return parameterspec
