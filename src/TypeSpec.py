from ClassName import ClassName
from CodeBlock import CodeBlock
from FieldSpec import FieldSpec
from TypeName import TypeName
from AnnotationSpec import AnnotationSpec
from multipledispatch import dispatch
from Util import Util


class TypeSpec:
    def __init__(self, builder):
        self.initializer_block = builder.initializer_block.build()
        self.static_block = builder.static_block.build()
        self.pythondoc = builder.pythondoc.build()
        self.annotations = builder.annotations  # self.annotations = Util.immutable_list(builder.annotations)
        self.anonymous_type_arguments = builder.anonymous_type_arguments
        self.field_specs = builder.field_specs  # self.field_specs = Util.immutable_list(builder.field_specs)
        self.method_specs = builder.method_specs  # self.method_specs = Util.immutable_list(builder.method_specs)
        self.type_specs = builder.type_specs  # self.type_specs = Util.immutable_list(builder.type_specs)
        self.superinterfaces = builder.superinterfaces  # self.superinterfaces = Util.immutable_list(builder.superinterfaces)
        self.superclass = builder.superclass
        self.name = builder.name
        self.type_variables = set()
        self.enum_constants = builder.enum_constants

    @staticmethod
    def class_builder(class_name):
        builder = Builder(class_name)
        return builder

    def emit(self, code_writer, enum_name):
        # Nested classes interrupt wrapped line indentation.
        # Stash the current wrapping state and put it back afterwards when this type is complete.
        previous_statement_line = code_writer.statement_line
        code_writer.statement_line = -1
        try:
            if enum_name:
                code_writer.emit_python_doc(self.pythondoc)
                code_writer.emit_annotations(self.annotations, False)
                code_writer.emit("$L", enum_name)
                if self.anonymous_type_arguments.format_parts:
                    code_writer.emit("(")
                    code_writer.emit(self.anonymous_type_arguments)
                    code_writer.emit(")")
                if self.field_specs and self.method_specs and self.type_specs:
                    return  # Avoid unnecessary braces "{}".
                code_writer.emit(" {\n")
            elif self.anonymous_type_arguments:
                supertype = not (self.superinterfaces and self.superinterfaces.get(0) or self.superclass)
                code_writer.emit("new $T(", supertype)
                code_writer.emit(self.anonymous_type_arguments)
                code_writer.emit(") {\n")
            else:
                # push an empty type (specifically without nested types) for type-resolution.
                code_writer.push_type(self)

                code_writer.emit_python_doc(self.pythondoc)
                code_writer.emit_annotations(self.annotations, False)

                # codeWriter.emitModifiers(modifiers, Util.union(implicitModifiers, kind.asMemberModifiers));
                # if (kind == Kind.ANNOTATION) {
                #   codeWriter.emit("$L $L", "@interface", name);
                # } else {
                #   codeWriter.emit("$L $L", kind.name().toLowerCase(Locale.US), name);
                # }
                code_writer.emit("class $L", self.name)
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
                #
                # if not extends_types:
                #     codeWriter.emit(" extends");
                #     boolean
                #     firstType = true;
                #     for (TypeName type: extendsTypes) {
                #       if (!firstType) codeWriter.emit(",");
                #       codeWriter.emit(" $T", type);
                #       firstType = false;
                #     }
                # if not implements_types:
                #     codeWriter.emit(" implements");
                #     boolean
                #     firstType = true;
                #     for (TypeName type: implementsTypes) {
                #       if (!firstType) codeWriter.emit(",");
                #       codeWriter.emit(" $T", type);
                #       firstType = false;
                #     }

                code_writer.pop_type()

                code_writer.emit(" :\n")

            code_writer.push_type(self)
            code_writer.indent_()
            first_member = True
            try:
                for i in iter(self.enum_constants):
                    enum_constant = next(i)
                    if not first_member:
                        code_writer.emit("\n")
                    # enumConstant.getValue().emit(codeWriter, enumConstant.getKey(), Collections.emptySet());
                    self.enum_constants.get(enum_constant).emit(code_writer, enum_constant)
                    first_member = False
                    if i:
                        code_writer.emit(",\n")
                    elif self.field_specs or self.method_specs or self.type_specs:
                        code_writer.emit(";\n")
                    else:
                        code_writer.emit("\n")
            except StopIteration:
                pass

            # Static fields.
            # for (FieldSpec fieldSpec: fieldSpecs) {
            #     if (!fieldSpec.hasModifier(Modifier.STATIC))  continue;
            #     if (!firstMember) codeWriter.emit("\n");
            #     fieldSpec.emit(codeWriter, kind.implicitFieldModifiers);
            #     firstMember = false;
            # }

            if self.static_block:
                if not first_member:
                    code_writer.emit("\n")
                code_writer.emit(self.static_block)
                first_member = False

            # Non-static fields.
            # for (FieldSpec fieldSpec: fieldSpecs) {
            #     if (fieldSpec.hasModifier(Modifier.STATIC))  continue;
            #     if (!firstMember) codeWriter.emit("\n");
            #     fieldSpec.emit(codeWriter, kind.implicitFieldModifiers);
            #     firstMember = false;
            # }

            # Initializer block.
            if self.initializer_block:
                if not first_member:
                    code_writer.emit("\n")
                code_writer.emit(self.initializer_block)
                first_member = False

            # Constructors.
            # for (MethodSpec methodSpec: methodSpecs) {
            #     if (!methodSpec.isConstructor())  continue;
            #     if (!firstMember) codeWriter.emit("\n");
            #     methodSpec.emit(codeWriter, name, kind.implicitMethodModifiers);
            #     firstMember = false;
            # }

            # Methods (static and non-static).
            for methodspec in self.method_specs:
                if not first_member:
                    code_writer.emit("\n")
                methodspec.emit(code_writer, self.name)
                first_member = False

            # Types.
            for typespec in self.type_specs:
                if not first_member:
                    code_writer.emit("\n")
                typespec.emit(code_writer, None)
                first_member = False

            code_writer.unindent_()
            code_writer.pop_type()

            code_writer.emit("}")
            if not enum_name and not self.anonymous_type_arguments:
                code_writer.emit("\n")  # If this type isn't also a value, include a trailing newline.
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
    initializer_block = CodeBlock.builder()
    static_block = CodeBlock.builder()
    enum_constants = dict()
    type_variables = list()

    def __init__(self, class_name):
        self.name = class_name

    def build(self):
        typespec = TypeSpec(self)
        return typespec

    def add_method(self, method_spec):
        # if (kind == Kind.INTERFACE) {
        #     requireExactlyOneOf(methodSpec.modifiers, Modifier.ABSTRACT, Modifier.STATIC, Modifier.DEFAULT);
        #     requireExactlyOneOf(methodSpec.modifiers, Modifier.PUBLIC, Modifier.PRIVATE);
        # }
        # else if (kind == Kind.ANNOTATION) {
        #     checkState(methodSpec.modifiers.equals(kind.implicitMethodModifiers),
        #         "%s %s.%s requires modifiers %s", kind, name, methodSpec.name, kind.implicitMethodModifiers);
        # }
        # if (kind != Kind.ANNOTATION) {
        #     checkState(methodSpec.defaultValue == null,
        #         "%s %s.%s cannot have a default value", kind, name, methodSpec.name);
        # }
        # if (kind != Kind.INTERFACE) {
        #     checkState(!methodSpec.hasModifier(Modifier.DEFAULT),
        #         "%s %s.%s cannot be default", kind, name, methodSpec.nam
        # }
        self.method_specs.append(method_spec)
        return self

    @dispatch(str, str)
    def add_python_doc(self, format1, *args):
        self.pythondoc.add(format1, args)
        return self

    @dispatch(CodeBlock)
    def add_python_doc(self, block):
        self.pythondoc.add(block)
        return self

    def add_type_variables(self, type_variables):
        # Util.check_state()
        # Util.check_argument()
        for type_variable in type_variables:
            self.type_variables.append(type_variable)
        return self

    def add_type_variable(self, type_variable):
        # Util.check_state()
        self.type_variables.append(type_variable)
        return self

    @dispatch(TypeName, str)
    def add_field(self, type1, name):
        return self.add_field(FieldSpec.builder(type1, name).build())

    @dispatch(FieldSpec)
    def add_field(self, field_spec):
        # if (kind == Kind.INTERFACE | | kind == Kind.ANNOTATION) {
        #   requireExactlyOneOf(fieldSpec.modifiers, Modifier.PUBLIC, Modifier.PRIVATE);
        #   Set < Modifier > check = EnumSet.of(Modifier.STATIC, Modifier.FINAL);
        #   checkState(fieldSpec.modifiers.containsAll(check),
        #               "%s %s.%s requires modifiers %s", kind, name, fieldSpec.name, check);
        # }
        self.field_specs.append(field_spec)
        return self

    @dispatch(TypeSpec)
    def add_type(self, type_spec):
        # Util.check_argument()
        self.type_specs.append(type_spec)
        return self

    @dispatch(list)
    def add_type(self, type_specs):
        # Util.checkArgument()
        for type_spec in type_specs:
            self.add_type(type_spec)
        return self

    def add_annotations(self, annotation_specs):
        for annotation_spec in annotation_specs:
            self.annotations.append(annotation_spec)
        return self

    @dispatch(AnnotationSpec)
    def add_annotation(self, annotation_spec):
        self.annotations.append(annotation_spec)
        return self

    @dispatch(ClassName)
    def add_annotation(self, annotation):
        return self.add_annotation(AnnotationSpec.builder(annotation).build())