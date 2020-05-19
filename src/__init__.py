from AnnotationSpec import AnnotationSpec
from MethodSpec import MethodSpec
from PythonFile import PythonFile
from TypeSpec import TypeSpec

method_name = 'service_name'
app_name = 'app'
url = 'service_url'
package_name = 'selab'
className = "controller"

methodspec = MethodSpec.method_builder(method_name)\
    .add_annotation(AnnotationSpec.builder(app_name).add_url_member(url).build())\
    .build()
type_spec = TypeSpec.class_builder(className).add_method(methodspec).build()

pythonfile = PythonFile.builder(package_name, type_spec).build()

pythonfile.write_to()