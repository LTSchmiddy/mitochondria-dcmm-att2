import os
import json
import ntpath


class ModBase:
    def __init__(self, pak_path):
        self.load_order = -1
        self.pak_path = pak_path
        self.display_name =  ntpath.basename(pak_path)[1]


class SteamMod:
    def __init__(self, path, steam_id):
        self.load_order = -1
        self.path = path
        self.metadata_path = self.path + "/settings.json"
        self.metadata = json.load(open(self.metadata_path , 'r'))

        self.image_path = self.get_image_path()
        self.pak_path = self.path + "/res.pak"

        self.steam_id = steam_id
        self.display_name = "STEAM: " + self.metadata["name"]


    def get_image_path(self):
        png_path = self.path + "/preview.png"

        if os.path.isfile(png_path):
            return png_path

        jpeg_path =  self.path + "/preview.jpg"
        if os.path.isfile(jpeg_path):
            return jpeg_path

        return None

