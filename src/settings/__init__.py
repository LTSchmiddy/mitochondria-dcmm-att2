# __all__

import sys
import os

import json

# print(sys.argv[0])


exec_dir, exec_file = os.path.split(os.path.abspath(sys.argv[0]))


def is_build_version():
    global exec_file
    return exec_file.endswith(".exe")


def is_source_version():
    global exec_file
    return exec_file.endswith(".py")


def get_exec_path(path):
    global exec_dir
    return os.path.join(exec_dir, path)


if is_source_version():
    path_arr = exec_dir.replace("\\", "/").split("/")
    exec_dir = "/".join(path_arr[: len(path_arr) - 1]).replace("/", "\\")

print(f"Is Source: {is_source_version()}")
print(f"Is Build: {is_build_version()}")
print(f"Exec Dir: {exec_dir}")

settings_path = "settings.json"

default_settings = {
    "window": {
        "x": None,
        "y": None,
        "width": None,
        "height": None,
        "web-engine": "cef",
    },
    "interface": {
        "app-root": "",
        "pages": {"template-dir": "templates", "static-dir": "static"},
        "view-panes": {
            "template-dir": "templates",
            # 'template-dir': "templates/view_pane_templates",
            "static-dir": "static",
        },
        "api": {"template-dir": "apl_templates", "static-dir": "static"},
        "flask-address": "127.0.0.1",
        "flask-port": 10000,
        "jquery-icon-mode": False,
    },
    "dirs": {
        "game_directory": "D:/Project Z/codenameVaporWareLib/steamapps/common/Dead _ Cells",
        "tools_dir": "D:/Project Z/codenameVaporWareLib/steamapps/common/Dead Cells/ModTools",
        "operating_dir": "./mdcmm",
        "saves_backup_dir": " saves",
        "game_save_dir": "./save",
        "sync_save_dir": "",
        "using_steam_sync": False,
        "extraction_profile": "extract",
        "steam_workshop_folder": "../../workshop/content/588650",
    },
    "files": {
        "main_pak": "res.pak",
        "master_pak": "res_master.pak",
        "master_backup_pak": "res_master_backup.pak",
        "main_pak_checksum": ""
    }
}

current = default_settings.copy()


def load_settings():
    global current
    current = default_settings.copy()

    def recursive_load(main, loaded):
        new_update_dict = {}

        # print(json.dumps(main, indent=4))

        for key, value in main.items():
            if not (key in loaded):
                continue

            if isinstance(value, dict):
                recursive_load(value, loaded[key])

            else:
                new_update_dict[key] = loaded[key]

        main.update(new_update_dict)

    # load preexistent settings file
    if os.path.exists(settings_path) and os.path.isfile(settings_path):
        imported_settings = json.load(open(settings_path, "r"))
        # current.update(imported_settings)
        recursive_load(current, imported_settings)

    # settings file not found
    else:
        save_settings()


def save_settings():
    global current
    json.dump(current, open(settings_path, "w"), indent=4)


def validate_settings() -> list:
    import settings.paths as p

    global current
    retVal = []

    if not os.path.isfile(p.get_game_exec()):
        retVal.append(
            [
                "game_exec_not_found",
                "'deadcells.exe' not found. Please set dirs->game_directory to path of your deadcells installation folder.",
            ]
        )

    if not os.path.isfile(p.get_pak_tool()) or not os.path.isfile(p.get_cdb_tool()):
        retVal.append(
            [
                "game_mod_tools_not_found",
                "The Deadcells modding toold were not found. Please set dirs->tools_dir to path of your deadcells modding tools folder. (This folder should be located in your Deadcells main installation folder.)",
            ]
        )

    return retVal


# load_settings()
from settings import paths
