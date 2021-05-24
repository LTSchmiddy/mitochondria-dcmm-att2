from py_anonymous_functions import *
import time

def do():
    print('doing')


# a = AnonFuncBasic("print('hello alex')")
a = AnonFuncBasic("print(args[0])")

a('argument')
# print(a())
