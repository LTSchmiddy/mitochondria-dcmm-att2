import sys
import multiprocessing

from data import std_handler
std_handler.init()

import settings.paths
from data.pak_tools import tool_man



if __name__ == '__main__':
    if sys.platform.startswith('win'):
        # On Windows calling this function is necessary.
        multiprocessing.freeze_support()

    # from data import std_handler


    settings.load_settings()

    # import generate_py_api
    # generate_py_api.rebuild_api()

    # bg_startup()

    import interface_flask
    import viewport


    viewport.create_window(False)
    interface_flask.start_server()


    # launches the main GUI loop:
    viewport.start_window()

    # Shuts down the application:
    print("CLOSED")


    interface_flask.stop_server()
    settings.save_settings()
    tool_man.on_quit()


    sys.exit(0)