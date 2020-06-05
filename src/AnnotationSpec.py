from CodeBlock import CodeBlock


class AnnotationSpec:
    def __init__(self, builder):
        self.type1 = builder.type1
        self.url = builder.url
        self.members = builder.members  # self.members = Util.immutable_multimap(builder.members)

    @staticmethod
    def builder(app_name):
        builder = Builder(app_name)
        return builder

    def emit(self, code_writer, inline):
        # print("AnnotationSpec.emit(code_writer, inline)")
        if inline is True:
            whitespace = ""
            member_separator = ", "
        else:
            whitespace = "\n"
            member_separator = ",\n"

        if not self.members:
            code_writer.emit("@$T", self.type1)
        elif len(self.members) == 1 and 'value' in self.members:
            code_writer.emit("@$T(", self.type1)
            self.emit_annotation_values(code_writer, whitespace, member_separator, self.members['value'])
            code_writer.emit(")")
        else:
            code_writer.emit("@$T(" + whitespace, self.type1)
            code_writer.indent_(2)
            # for (Iterator < Map.Entry < String, List < CodeBlock >> > i = members.entrySet().iterator(); i.hasNext(); )
            # {
            #     Map.Entry < String, List < CodeBlock >> entry = i.next();
            #     codeWriter.emit("$L = ", entry.getKey());
            #     emitAnnotationValues(codeWriter, whitespace, memberSeparator, entry.getValue());
            #     if (i.hasNext())
            #         codeWriter.emit(memberSeparator);
            # }
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
    app_name = ''
    url = ''
    members = dict()

    def __init__(self, app_name):
        if app_name != '':
            self.app_name = app_name
            self.type1 = 'route'

    def add_url_member(self, url):  # add url here
        codeblock = CodeBlock.add_url(url)
        return self

    def build(self):
        annotationspec = AnnotationSpec(self)
        return annotationspec

    def add_member(self, name, code_block):
        # Util.check_not_null()
        # Util.check_argument()
        # List < CodeBlock > values = members.computeIfAbsent(name, k -> new ArrayList <> ());
        values = list()
        if name not in self.members.keys():
            self.members[name] = values
        values.append(code_block)
        return self
