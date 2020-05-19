from CodeBlock import CodeBlock
from TypeName import TypeName
from Util import Util


class TypeSpec:
    def __init__(self, builder):
        self.pythondoc = builder.pythondoc.build()
        self.annotations = Util.immutable_list(builder.annotations)
        self.anonymous_type_arguments = builder.anonymous_type_arguments
        self.field_specs = Util.immutable_list(builder.field_specs)
        self.method_specs = builder.method_specs  # self.method_specs = Util.immutable_list(builder.method_specs)
        self.type_specs = builder.type_specs  # self.type_specs = Util.immutable_list(builder.type_specs)
        self.superinterfaces = Util.immutable_list(builder.superinterfaces)
        self.superclass = builder.superinterfaces
        self.name = builder.name
        self.type_variables = set()

    @staticmethod
    def class_builder(class_name):
        builder = Builder(class_name)
        return builder

    def emit(self, code_writer, enum_name):
        previous_statement_line = code_writer.statement_line
        code_writer.statement_line = -1
        try:
            if enum_name is not None:
                code_writer.emit_python_doc(self.pythondoc)
                code_writer.emit_annotations(self.annotations, False)
                code_writer.emit("$L", enum_name)
                if self.anonymous_type_arguments.format_parts.is_empty():
                    code_writer.emit("(")
                    code_writer.emit(self.anonymous_type_arguments)
                    code_writer.emit(")")
                if self.field_specs.is_empty() and self.method_specs.is_empty() and self.type_specs.is_empty():
                    return  # Avoid unnecessary braces "{}".
                code_writer.emit(" {\n")
            elif self.anonymous_type_arguments is not None:
                supertype = not (self.superinterfaces and self.superinterfaces.get(0) or self.superclass)
                code_writer.emit("new $T(", supertype)
                code_writer.emit(self.anonymous_type_arguments)
                code_writer.emit(") {\n")
            else:
                """
                code_writer.push_type(TypeSpec(self))

                code_writer.emit_python_doc(self.pythondoc)
                code_writer.emit_annatations(self.annotations, False)
                """
                # codeWriter.emitModifiers(modifiers, Util.union(implicitModifiers, kind.asMemberModifiers));
                # if (kind == Kind.ANNOTATION) {
                #   codeWriter.emit("$L $L", "@interface", name);
                # } else {
                #   codeWriter.emit("$L $L", kind.name().toLowerCase(Locale.US), name);
                # }
                code_writer.emit_type_variables(self.type_variables)
                # extends_types = list()
                # implements_types = list()
                # if (kind == Kind.INTERFACE) {
                #   extendsTypes = superinterfaces;
                #   implementsTypes = Collections.emptyList();
                # } else {
                # extendsTypes = superclass.equals(ClassName.OBJECT)
                #   ? Collections.emptyList()
                #   : Collections.singletonList(superclass);
                # implementsTypes = superinterfaces;
                # }

                # if not extends_types:
                    # codeWriter.emit(" extends");
                    # boolean
                    # firstType = true;
                    # for (TypeName type: extendsTypes) {
                    # if (!firstType) codeWriter.emit(",");
                    # codeWriter.emit(" $T", type);
                    # firstType = false;
                    # }
                # if not implements_types:
                    # codeWriter.emit(" implements");
                    # boolean
                    # firstType = true;
                    # for (TypeName type: implementsTypes) {
                    # if (!firstType) codeWriter.emit(",");
                    # codeWriter.emit(" $T", type);
                    # firstType = false;
                    # }

                code_writer.pop_type()

                code_writer.emit(" {\n")

            code_writer.push_type(self)
            code_writer.indent  # NoneType error here if statement is: code_writer.indent()
            first_member = True
            """for (Iterator<Map.Entry<String, TypeSpec>> i = enumConstants.entrySet().iterator(); i.hasNext(); ) {
                Map.Entry<String, TypeSpec> enumConstant = i.next();
                if (!firstMember) codeWriter.emit("\n");
                enumConstant.getValue().emit(codeWriter, enumConstant.getKey(), Collections.emptySet());
                firstMember = false;
                if (i.hasNext()) {
                    codeWriter.emit(",\n");
                } else if (!fieldSpecs.isEmpty() || !methodSpecs.isEmpty() || !typeSpecs.isEmpty()) {
                    codeWriter.emit(";\n");
                } else {
                    codeWriter.emit("\n");
                }
            }"""
            # Methods
            # for methodspec in self.method_specs:
            #     if not first_member:
            #         code_writer.emit("\n")
            #     methodspec.emit(code_writer, self.name)
            #     first_member = False

            # Types
            # for typespec in self.type_specs:
            #     if not first_member:
            #         code_writer.emit("\n")
            #     typespec.emit(code_writer, None)
            #     first_member = False

            code_writer.unindent()
            code_writer.pop_type()

            code_writer.emit("}")
            if enum_name is None and self.anonymous_type_arguments is None:
                code_writer.emit("\n")
        finally:
            code_writer.statement_line = previous_statement_line


class Builder:
    pythondoc = CodeBlock.builder()
    annotations = list()
    anonymous_type_arguments = None  # private final CodeBlock anonymous_type_arguments
    type_specs = list()
    method_specs = list()
    field_specs = list()
    superclass = TypeName
    superinterfaces = list()
    name = str()

    def __init__(self, class_name):
        self.name = class_name

    def build(self):
        typespec = TypeSpec(self)
        return typespec

    def add_method(self, method_spec):
        self.method_specs.append(method_spec)
        return self
