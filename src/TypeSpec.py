class TypeSpec:
    def __init__(self, builder):
        print()

    @staticmethod
    def class_builder(class_name):
        builder = Builder(class_name)
        return builder

    def emit(self, code_writer, enum_name):
        print()


class Builder:
    def __init__(self, class_name):
        print()

    def build(self):
        typespec = TypeSpec(self)
        return typespec

    def add_method(self, method_spec):
        return self
