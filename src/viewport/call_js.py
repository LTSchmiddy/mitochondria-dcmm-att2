import sys
import os
import threading

import interface_flask

import webview as wv

import viewport.js_api
import viewport.bg_tasks

import settings

scripts_directory = settings.get_exec_path("calljs/")

if settings.is_source_version():
    scripts_directory = settings.get_exec_path("viewport/call_js_scripts/")



class CallJS:
    path: str
    script: str

    def __init__(self, path):
        self.path = path
        self.script = open(scripts_directory + path, 'r').read()

    def run(self):
        return viewport.window.evaluate_js(self.script)
