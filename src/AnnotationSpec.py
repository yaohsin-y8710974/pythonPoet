from multipledispatch import dispatch
from CodeBlock import CodeBlock


class AnnotationSpec:
    app_name = ''

    def __init__(self, builder):
        self.type1 = builder.type1
        self.url = builder.url
        self.members = builder.members  # self.members = Util.immutable_multimap(builder.members)
        self.annotation_name = builder.annotation_name

    @staticmethod
    def builder(annotation_name):
        builder = Builder(annotation_name)
        return builder

    def emit(self, code_writer, inline):
        if inline is True:
            whitespace = ""
            member_separator = ", "
        else:
            whitespace = "\n"
            member_separator = ",\n"

        if self.type1:  # emit of @route annotation
            code_writer.emit("@")
            code_writer.emit("$L", AnnotationSpec.app_name)
            code_writer.emit(".")
            code_writer.emit("$L", self.type1)
            code_writer.emit("('")
            code_writer.emit(self.url)
            code_writer.emit("')")
        else:  # emit other annotations
            self.type1 = self.annotation_name
            if not self.members:
                code_writer.emit("@$T", self.type1)
            elif len(self.members) == 1 and 'value' in self.members:
                code_writer.emit("@$T(", self.type1)
                self.emit_annotation_values(code_writer, whitespace, member_separator, self.members['value'])
                code_writer.emit(")")
            else:
                code_writer.emit("@$T(" + whitespace, self.type1)
                code_writer.indent_(2)

                for i in self.members:
                    entry = next(i)
                    code_writer.emit("$L = ", entry)
                    self.emit_annotation_values(code_writer, whitespace, member_separator, self.members[entry])
                    if next(i):
                        code_writer.emit(member_separator)
                    else:
                        pass

                code_writer.unindent_(2)
                code_writer.emit(whitespace + ")")

    def emit_annotation_values(self, code_writer, whitespace, member_separator, values):
        if len(values) == 1:
            code_writer.indent_(2)
            code_writer.emit(values[0])
            code_writer.unindent(2)
            return

        code_writer.emit("{" + whitespace)
        code_writer.indent_(2)
        first = True
        for code_block in values:
            if not first:
                code_writer.emit(member_separator)
            code_writer.emit(code_block)
            first = False
        code_writer.unindent_(2)
        code_writer.emit(whitespace + "}")


class Builder:
    type1 = ''
    annotation_name = ''
    url = ''
    members = dict()

    def __init__(self, annotation_name):
        if annotation_name != 'route':
            self.type1 = None
            self.annotation_name = annotation_name
        else:
            self.type1 = 'route'

    def build(self):
        annotationspec = AnnotationSpec(self)
        return annotationspec

    @dispatch(str, str, str)
    def add_member(self, name, format1, *args):
        return self.add_member(name, CodeBlock.of(format1, args))

    @dispatch(str)
    def add_url(self, url):
        self.url = url
        return self

    @dispatch(str, CodeBlock)
    def add_member(self, name, code_block):
        # Util.check_not_null()
        # Util.check_argument()
        # List < CodeBlock > values = members.computeIfAbsent(name, k -> new ArrayList <> ());
        values = list()
        if name not in self.members.keys():
            self.members[name] = values
        values.append(code_block)
        return self

    def set_app_name(self, app_name):
        AnnotationSpec.app_name = app_name
        return self
