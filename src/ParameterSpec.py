from TypeName import TypeName
from Util import Util


class ParameterSpec():
    name =""
    annotations = list()
    modifiers = set()
    type = TypeName

    def __init__(self, builder):
        # self.name = builder.name
        # self.annotations = Util.immutable_list(builder.annotations)
        # self.modifiers = Util.immutable_set(builder.modifiers)
        # self.type = builder.type
        print()

    @staticmethod
    def builder():
        # check_not_null()
        # check_argument()
        return ParameterSpec.Builder()

    class Builder:
        def __init__(self):
            print("parameterspec builder")

        def build(self, parameter_name):
            parameter_spec = ParameterSpec(ParameterSpec.Builder)
            return parameter_spec