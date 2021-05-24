from __future__ import annotations

import os
import threading
import time
import shutil

import webview as wv
import viewport
import interface_flask

import settings
import settings.paths
from cefpython3 import cefpython as cef
from viewport.bg_tasks import bg_startup
from data import pak_tools, std_handler, saves, deadcells_game

class CefCallback:
    known_callbacks = []

    def __init__(self):
        pass

    @classmethod
    def add_callback(cls, cb: CefCallback):
        cls.known_callbacks.append(cb)