from TypeName import TypeName
from Util import Util


class ParameterSpec:
    name = ""
    annotations = list()
    modifiers = set()
    type = TypeName

    def __init__(self, builder):
        self.name = builder.name
        self.annotations = builder.annotations  # self.annotations = Util.immutable_list(builder.annotations)
        # self.modifiers = Util.immutable_set(builder.modifiers)
        self.type = builder.type

    @staticmethod
    def builder(parameter_name):
        builder = Builder(parameter_name)
        return builder


class Builder:
    type = TypeName
    name = str()
    annotations = list()

    def __init__(self, parameter_name):
        print()

    def build(self):
        parameterspec = ParameterSpec(self)
        return parameterspec
