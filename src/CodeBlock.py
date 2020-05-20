from Util import Util


class CodeBlock:
    def __init__(self, builder):
        self.format_parts = builder.format_parts  # self.format_parts = Util.immutable_list(builder.format_parts)
        self.args = builder.args  # self.args = Util.immutable_list(builder.args)

    @staticmethod
    def builder():  # done
        builder = Builder()
        return builder

    @classmethod
    def add_url(cls, url):
        builder = Builder().url(url).build()
        return builder

    def is_empty(self):
        return not self.format_parts

    def of(self, format, args):
        builder = Builder()
        return builder.add(format, args).build()


class Builder:
    format_parts = list()
    args = list()

    def build(self):  # done
        codeblock = CodeBlock(self)
        return codeblock

    def url(self, url):
        self.args.append(url)
        return self

    def add_statement(self, code_block):
        return self

    def add(self, format, args):
        return self
