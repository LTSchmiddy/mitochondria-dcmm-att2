import sys
import os
import io
import typing
import types
import string
from typing import List

from ansi2html import Ansi2HTMLConverter

custom_loggers = []
allowed_chars = """0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\\\'()*+,-./:;<=>?@[]^_`{|}~ \t\n"""

class CustomStdout:
    stream: str
    # old_stdout: io.TextIOWrapper
    substreams: List[io.TextIOWrapper]

    def __init__(self, old_stdout = None, use_file = True):
        global custom_loggers
        self.level = "INFO"
        self.substreams = []

        self.html_converter = Ansi2HTMLConverter(inline=True)

        if old_stdout is not None:
            self.substreams.append(old_stdout)
        if use_file:
            self.substreams.append(open('out.log', 'w'))

        self.stream = ""
        self.stream_sanatized = ""
        self.stream_html = ""

        custom_loggers.append(self)

    def write(self, data):
        self.stream += data
        # self.old_stdout.write("OUT: " + data)
        for i in self.substreams:
            i.write(data)

        self.write_sanitized(data)
        self.write_html(data)

    def write_sanitized(self, data):
        # to_write = str(data)
        # processed_char = []
        # for i in str(data)
        global allowed_chars
        self.stream_sanatized += ''.join(filter(lambda x: x in allowed_chars, str(data)))

        # self.old_stdout.write(data)

    def write_html(self, data):
        self.stream_html += self.html_converter.convert(str(data), full=False)
        # self.stream_html = self.html_converter.convert(self.stream, full=False)
        # self.stream_html = self.html_converter.convert(self.stream)

    def flush(self):
        for i in self.substreams:
            i.flush()


    def get_all(self):
        return self.stream

    def get_sanitized(self):
        return self.stream_sanatized

    def get_html(self):
        return self.stream_html

    # def get_converted_html(self):
    #     return self.html_converter.convert(self.stream)



my_stdout = CustomStdout(sys.stdout)
def init():
    global my_stdout
    sys.stdout = my_stdout