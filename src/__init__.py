from AnnotationSpec import AnnotationSpec
from MethodSpec import MethodSpec
from PythonFile import PythonFile
from TypeSpec import TypeSpec

app_name = 'app'
method_name = 'test_method'
url = 'service_url'
package_name = 'selab'
className = "FlaskController"

methodspec = MethodSpec.method_builder(method_name) \
    .add_annotation(AnnotationSpec.builder("route").add_url(url).set_app_name(app_name).build()) \
    .add_parameter("args")\
    .add_statement("instanceInvoker = Invoker()")\
    .add_statement("service_input = request.args.get('serviceInput')")\
    .begin_control_flow("if not(ServiceUtilObject.hasID('requestWrapper, storage'))")\
    .add_statement("return 'error message: there is no this ID'")\
    .end_control_flow()\
    .add_statement("ServiceUtilObject = ServiceUtilObject(requestWrapper, storage, 'database')")\
    .add_statement("ServiceUtilObject.loadDependency('--python dependency--')")\
    .add_statement("invokerResult = instanceInvoker.service_name(serviceUtilObject, service_input)")\
    .add_statement("return invokerResult")\
    .build()

type_spec = None
TypeSpec.methods.append(methodspec)  # append methodSpec if TypeSpec is None
pythonfile = PythonFile.builder(package_name, type_spec).build()

controller_writer = open("Controller.py", 'w')
pythonfile.write_to(controller_writer)
controller_writer.close()

print('----------------------------------------------------------')

methodName = 'someMethod__type_of_param1__type_of_param2'
packageName = 'pickle'

methodSpec = MethodSpec.method_builder(methodName)\
    .add_parameter('component')\
    .add_parameter('_self')\
    .add_parameter('param1')\
    .add_parameter('param2')\
    .add_statement('obj = pickle.loads(_self)')\
    .add_statement('method = getattr(obj, "someMethod")')\
    .add_statement('return pickle.dumps(method(param1, param2))')\
    .build()

typeSpec = None
TypeSpec.methods = list()  # clear all methods in TypeSpec.methods
TypeSpec.methods.append(methodSpec)
pythonFile = PythonFile.builder(packageName, typeSpec).build()

invoker_writer = open("invoker.py", 'w')
pythonFile.write_to(invoker_writer)
invoker_writer.close()
