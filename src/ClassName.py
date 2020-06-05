from TypeName import TypeName


class ClassName(TypeName):
    canonical_name = str

    def __init__(self, keyword, annotations):
        super().__init__(keyword, annotations)

    @classmethod
    def package_name(cls):
        pass

    @classmethod
    def without_annotations(cls):
        pass

    def emit(self, out):
        char_emitted = False
        for class_name in self.enclosing_classes():
            simple_name = str
            if char_emitted:
                # We've already emitted an enclosing class. Emit as we go.
                out.emit(",")
                simple_name = class_name.simple_name
            elif class_name.is_annotated() or class_name == self:  # not finish yet
                # We encountered the first enclosing class that must be emitted.
                qualified_name = out.lookup_name(class_name)
            # int dot = qualifiedName.lastIndexOf('.');
            # if (dot != -1) {
            #     out.emitAndIndent(qualifiedName.substring(0, dot + 1));
            #     simpleName = qualifiedName.substring(dot + 1);
            #     charsEmitted = true;
            # }
            # else {
            #     simpleName = qualifiedName;
            # }
            else:
                # Don't emit this enclosing type. Keep going so we can be more precise.
                continue

            # if (className.isAnnotated()) {
            #     if (charsEmitted) out.emit(" ");
            #         className.emitAnnotations(out);
            # }
            #
            # out.emit(simpleName);
            # charsEmitted = true;

        return out

    # Returns all enclosing classes in this, outermost first.
    def enclosing_classes(self):
        result = list()
        for c in self.enclosing_classes():
            result.append((c))
        result.reverse()  # Collections.reverse(result);
        return result

    def top_level_class_name(self):
        if self.enclosing_class_name:
            return self.enclosing_class_name.top_level_class_name()
        else:
            return self
