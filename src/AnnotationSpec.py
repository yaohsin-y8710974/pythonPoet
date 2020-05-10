from CodeBlock import CodeBlock
from Util import Util


class AnnotationSpec:
    def __init__(self, builder):
        self.type = builder.type
        self.url = builder.url

    @staticmethod
    def builder(app_name):
        builder = Builder(app_name)
        return builder


class Builder:
    type = ''
    app_name = ''
    url = ''
    members = dict()

    def __init__(self, app_name):
        if app_name != '':
            self.app_name = app_name
            self.type = 'route'

    def add_url_member(self, url):  # add url here
        # Util.check_not_null()
        # Util.check_argument()
        codeblock = CodeBlock.add_url(url)
        return self

    def build(self):
        annotationspec = AnnotationSpec(self)
        return annotationspec
