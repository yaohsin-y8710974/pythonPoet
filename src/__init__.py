from AnnotationSpec import AnnotationSpec
from MethodSpec import MethodSpec
from PythonFile import PythonFile
from TypeSpec import TypeSpec
app_name = 'app_name'
method_name = 'test_method'
url = 'service_url'
package_name = 'selab'
className = "FlaskController"

# methodspec = MethodSpec.method_builder(method_name) \
#     .add_annotation(AnnotationSpec.builder(app_name).add_member(url).build()) \
#     .add_parameter("args")\
#     .build()

methodspec = MethodSpec.method_builder(method_name) \
    .add_parameter("argument")\
    .build()

type_spec = TypeSpec.class_builder(className)\
    .add_method(methodspec) \
    .build()

pythonfile = PythonFile.builder(package_name, type_spec).build()

writer = open("Controller.py", 'w')
pythonfile.write_to(writer)
writer.close()
