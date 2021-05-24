import types


# tool_man = toolwrapper.ToolMan

# class JsApi(object):
class JsApi:
    api_struct = {}

    def __init__(self):
        pass
        # self.tool_man = toolwrapper.tool_man

    @classmethod
    def remove_attr(cls, name):
        return delattr(cls, name)

    @classmethod
    def add_attr(cls, func, name = None):
        if name is None:
            name = func.__name__

        funcPath = name.split("__")

        funcNode = cls.api_struct
        for i in range(0, len(funcPath) - 1):
            if not (funcPath[i] in funcNode):
                funcNode[funcPath[i]] = {}

            funcNode = funcNode[funcPath[i]]

        funcNode[funcPath[len(funcPath) - 1]] = None

        return setattr(cls, name, types.MethodType(func, cls))

    @classmethod
    def add_module_method(cls, module_header: str, method: callable):
        if hasattr(method, "__name__"):
            use_name = module_header.replace(".", "__") + "__" + method.__name__
            # print(f"adding function {i} as {use_name}")

            # if attr_mode:
            try:
                cls.add_attr(method, use_name)
            except TypeError as e:
                print(f"{method.__name__}: {e}")

        else:
            print(f"Error in loading JsApi: '{method}' is has no __name__")

    @classmethod
    def add_anonymous_module_method(cls, module_header: str, m_name: str, method: callable):
            use_name = module_header.replace(".", "__") + "__" + m_name.__name__
            # print(f"adding function {i} as {use_name}")
            try:
                cls.add_attr(method, use_name)
            except TypeError as e:
                print(f"{method.__name__}: {e}")

    @classmethod
    def add_module_method_list(cls, module_header: str, method_list: list):
        for i in method_list:
            if isinstance(i, tuple):
                cls.add_anonymous_module_method(module_header, i[0], i[1])

            elif hasattr(i, "__name__"):
                cls.add_module_method(module_header, i)

            else:
                print(f"Error in loading JsApi: js_api could not process data '{str(i)}"'')




from viewport.js_api import method_loading

# Here, we load in modules too big to put into this file:
method_loading.create_api_modules(JsApi)



main_api = JsApi()



def process_js_bindings():
    pass
    # instance = viewport.get_cef_instance()
    # bindings: cef.JavascriptBindings = instance.GetJavascriptBindings()
    #
    # bindings.SetFunction("sleep", viewport.window.expose())
    #
    # bindings.Rebind()
