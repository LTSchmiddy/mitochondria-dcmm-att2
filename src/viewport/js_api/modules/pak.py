import os
import json

from typing import Type

# import viewport
from data import pak_tools

from viewport.js_api import JsApi
import viewport
import settings.paths


def create_pak_module(api: Type[JsApi]):
    # PakTool Module:
    def rebuild_all(self, *args):
        pak_tools.tool_man.run_rebuild_all(*args)

    def unpack_all(self, *args):
        pak_tools.tool_man.run_unpack_all(*args)

    def is_mproc_running(self):
        return pak_tools.tool_man.is_mproc_all_running()


    def unpack_pak(self, *args):
        pak_tools.tool_man.run_extract_pak(*args)

    def rebuild_pak(self, *args):
        pak_tools.tool_man.run_rebuild_pak(*args)

    def is_paktool_running(self):
        return pak_tools.tool_man.is_paktool_running()


    def unpack_cdb(self, *args):
        pak_tools.tool_man.run_extract_cdb(*args)

    def rebuild_cdb(self, *args):
        pak_tools.tool_man.run_rebuild_cdb(*args)

    def is_cdbtool_running(self):
        return pak_tools.tool_man.is_cdbtool_running()


    def unpack_all_from_master(self):
        pak_tools.tool_man.run_unpack_all(settings.paths.get_master_pak())

    api.add_module_method_list("pak", [
        rebuild_all,
        unpack_all,
        is_mproc_running,
        unpack_pak,
        rebuild_pak,
        is_paktool_running,
        unpack_cdb,
        rebuild_cdb,
        is_cdbtool_running,
        unpack_all_from_master
    ])


