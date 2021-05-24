from __future__ import annotations
from types import FunctionType
import inspect


# This function simply redirects the execution to one of the factory functions based on the given parameters:
def anon_func(*f_args, **f_kwargs) -> FunctionType:
    pass
    # anonymous_function.__code__ = compile(code, anonymous_function.__name__, 'exec')
    # return anonymous_function


def anon_func_basic_str(code: str)-> FunctionType:
    def anonymous_function(*args, **kwargs): pass
    # for i in inspect.stack():
    #     print(i)

    anonymous_function.__code__ = compile(code, f"<{anonymous_function.__name__}>", 'exec')
    return anonymous_function


# class AnonFunc(FunctionType):
    # def __init__(self, code: str, globals: Dict[str, Any]):
    #     super().__init__(code, globals)

class AnonFuncBasic:
    def __init__(self, code: str):
        self.compiled_code = compile(code, '<anonymous function>', 'exec')

    def __call__(self, *args, **kwargs):
        exec_globals = {
            'retVal': None,
            'args': args,
            'kwargs': kwargs
        }
        exec_globals.update(inspect.stack()[1].frame.f_globals)
        exec(self.compiled_code, exec_globals)

        return exec_globals['retVal']