from AnnotationSpec import AnnotationSpec
from MethodSpec import MethodSpec
from PythonFile import PythonFile
from TypeSpec import TypeSpec

method_name = 'main'
app_name = 'app'
url = 'service_url'
package_name = 'python_poet'
className = "class_name"

methodspec = MethodSpec.method_builder(method_name) \
    .add_annotation(AnnotationSpec.builder(app_name).add_url_member(url).build()) \
    .add_parameter("args")\
    .build()
type_spec = TypeSpec.class_builder(className)\
    .add_method(methodspec) \
    .build()

pythonfile = PythonFile.builder(package_name, type_spec).build()

writer = open("Controller.py", 'w')
pythonfile.write_to(writer)
writer.close()
