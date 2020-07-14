import sys
import os
import io
import typing
import types




# class StdIOIntercept(object):
T = typing.TypeVar('T')
class StdIOIntercept(object):
    class StdIOSet(typing.Generic[T]):
        stdin: T
        stdout: T
        stderr: T

        mode: str

        def __init__(self, mode='old', custom_args=()):
            # if mode == 'old':
            #     self.stdin = sys.stdin
            #     self.stdout = sys.stdout
            #     self.stderr = sys.stderr

            self.mode = mode

            if mode == 'main':
                self.stdin = io.StringIO()
                self.stdout = io.StringIO()
                self.stderr = io.StringIO()

            if mode == 'custom-type':
                self.stdin = T(*custom_args)
                self.stdout = T(*custom_args)
                self.stderr = T(*custom_args)

            else:
                # if mode == 'old':
                self.stdin = sys.stdin
                self.stdout = sys.stdout
                self.stderr = sys.stderr


        def activate(self):
            sys.stdin = self.stdin
            sys.stdout = self.stdout
            sys.stderr = self.stderr

        def is_active(self):
            if sys.stdin != self.stdin:
                return False

            if sys.stdout != self.stdout:
                return False

            if sys.stderr != self.stderr:
                return False

            return True


    old: StdIOSet[type(sys.stdout)]
    main: StdIOSet[io.StringIO]

    def __init__(self):
        self.old = StdIOIntercept.StdIOSet[type(sys.stdout)]('old')
        self.main = StdIOIntercept.StdIOSet[io.StringIO]('main')

        self.main.activate()
        print(self.main.is_active())


std_main: StdIOIntercept = None

def activate():
    global std_main
    std_main = StdIOIntercept()