from TypeName import TypeName


class ArrayTypeName(TypeName):
    def __init__(self, keyword, annotations):
        super().__init__(keyword, annotations)
        print()