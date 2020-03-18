class MethodSpec:
    def methodBuilder(self):
        self.Builder()

    parameters = list()
    class Builder:
        def __init__(self, methodName):
            print(methodName)

        def returns(self, returnType):
            print(returnType)

        def addParameter(parameterName):
            print(parameterName)
            MethodSpec.parameters.append(parameterName)

        def addStatement(statement):
            print(statement)

        @staticmethod
        def build():
            # build method and clear parameters
            print(MethodSpec.parameters)
            MethodSpec.parameters.clear()
