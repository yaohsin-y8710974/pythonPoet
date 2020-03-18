from methodSpec import MethodSpec

test = MethodSpec()
MethodSpec.Builder("methodName1")
test.Builder.addParameter("parameter1")
test.Builder.addStatement("a=1")
test.Builder.build()

print("===========================")

test2 = MethodSpec()
MethodSpec.Builder("methodName2")
test2.Builder.addParameter("parameter2")
test2.Builder.addStatement("a=2")
test2.Builder.build()