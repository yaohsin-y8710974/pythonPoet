class TypeName:
    keyword = str()
    annotations = list()

    def __init__(self, keyword, annotations):
        if annotations is not None:
            self.keyword = keyword
            self.annotations = list()
        else:
            self.keyword = keyword
            self.annotations = annotations

    def emit(self, out):
        if not self.keyword:
            raise AssertionError

        if self.is_annotated():
            out.emit("")
            self.emit_annotations(out)
        return out.emit_and_indent(self.keyword)

    def is_annotated(self):
        return self.annotations

    def emit_annotations(self, out):
        for annotationspec in self.annotations:
            annotationspec.emit(out, True)
        out.emit(" ")
        return out

    # Returns {@code type} as an array, or null if {@code type} is not an array.
    @staticmethod
    def as_array(type1):
        if isinstance(type1, ArrayTypeName):
            return type1
        else:
            return None
