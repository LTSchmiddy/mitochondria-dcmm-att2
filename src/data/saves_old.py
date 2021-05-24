import os
import sys
import shutil
import ntpath
from settings import current, paths
import datetime
import viewport
import pickle
from enum import IntEnum

default_num_save_slots = 7

def get_save_name(slot: int) -> str:
    return f"user_{slot}.dat"

def get_game_save_path(slot: int) -> str:
    return os.path.join(paths.get_game_save_dir(), get_save_name(slot)).replace("\\", "/")


# return {
#     'name': filename,
#     'path': path,
#     'type': filename_list[0],
#     'original_user': int(filename_list[1]),
#     'timestamp': use_timestamp,
#     'timestamp_source': stamp_source,
#     'datetime': str(datetime.datetime.fromtimestamp(float(use_timestamp))).split('.')[0],
#     'size': os.path.getsize(path),
#     'size_kb': int(os.path.getsize(path) / 1000)
# }

class SaveType(IntEnum):
    game_save = 0
    injected_save = 1

class SaveBackup:
    filepath: str
    file_timestamp: float

    save_type : SaveType

    original_user: int
    original_timestamp: float

    save_data: bytes

    def __init__(self):
        self.filepath = None

    @staticmethod
    def load_from_path(path):
        if not os.path.isfile(path):
            return None

        loaded_backup: SaveBackup = pickle.load(path)
        loaded_backup.filepath = path
        loaded_backup.file_timestamp = os.path.getmtime(path)

        return loaded_backup

    @staticmethod
    def make_from_game_save(game_save_path):
        if not os.path.isfile(game_save_path):
            return None

        new_backup = SaveBackup()

        # getting file metadata:
        new_backup.file_timestamp = datetime.datetime.now().timestamp()

        new_backup.original_timestamp = os.path.getmtime(game_save_path)
        new_backup.original_user = int(ntpath.basename(game_save_path).split("_")[1].split('.')[0])
        new_backup.save_type = SaveType.game_save

        # getting savedata:
        game_save_file = open(game_save_path, 'rb')
        new_backup.save_data = game_save_file.read()
        game_save_file.close()

        new_backup.save_to_disk()



    @property
    def filename(self) -> str:
        return ntpath.basename(self.filepath)

    @property
    def original_datetime(self) -> datetime.datetime:
        return datetime.datetime.fromtimestamp(self.original_timestamp)

    @property
    def original_datetime_str(self) -> str:
        return str(self.original_timestamp)

    @property
    def file_datetime(self) -> datetime.datetime:
        return datetime.datetime.fromtimestamp(self.file_timestamp)

    @property
    def file_datetime_str(self) -> str:
        return str(self.file_timestamp)

    @property
    def data_size(self) -> int:
        return len(self.save_data)

    @property
    def data_size_kb(self) -> int:
        return int(len(self.save_data)/1000)

    @property
    def exists_on_disk(self):
        return os.path.isfile(self.filepath)

    @property
    def is_saved_to_disk(self):
        return self.exists_on_disk and self.file_timestamp == os.path.getmtime(self.filepath)

    def generate_file_name(self, set_filepath: bool = False):
        retVal = ""
        if self.save_type == SaveType.game_save:
            retVal = f"""user_{self.original_user}_{str(self.original_timestamp).replace(".", "_")}.mdcs"""

        else:
            retVal = f"""injected_{self.original_user}_{str(self.file_timestamp).replace(".", "_")}.mdcs"""

        retPath = paths.get_save_slot_backup_dir(self.original_user) + f'/{retVal}'
        if set_filepath:
            self.filepath = retPath

        return retVal, retPath

    def save_to_disk(self):
        if self.filepath is None:
            self.generate_file_name(True)

        outfile = open(self.filepath, 'wb')
        pickle.dump(self, outfile)
        outfile.close()


class SavesMan:
    def __init__(self, num_save_slots = default_num_save_slots):
        self.num_save_slots = num_save_slots
        self.run_monitor = True

        self.last_mtimes = [0] * self.num_save_slots

        self.latest_save_file_backups = []
        self.latest_current_save_files = []

    @property
    def latest_backup(self):
        if len(self.latest_save_file_backups) == 0: return None
        return self.latest_save_file_backups[0]


    def monitor_all_saves(self):
        if not self.run_monitor:
            return

        for i in range(0, self.num_save_slots):
            self.monitor_save_slot(i)

    def monitor_save_slot(self, slot: int):
        if not self.run_monitor:
            return

        if not os.path.isfile(get_game_save_path(slot)):
            return

        if len(os.listdir(paths.get_save_slot_backup_dir(slot))) == 0:
            self.make_save_backup(slot)
        else:
            if self.last_mtimes[slot] == 0:
                self.last_mtimes[slot] = self.list_backup_saves(slot)[0]['timestamp']

        if os.path.getmtime(get_game_save_path(slot)) > self.last_mtimes[slot]:
            self.make_save_backup(slot)
            print(f"Save slot {slot} updated. Backing up...")
            self.update_last_mtime(slot)


    def make_save_backup(self, slot: int, is_injected: bool = False):
        f_heading = f"user_{slot}_"
        if is_injected:
            f_heading = f"injected_{slot}_"

        save_mtime = os.path.getmtime(get_game_save_path(slot))

        backup_filename = f_heading + str(save_mtime).replace(".", "-") + ".dat"
        backup_filepath = os.path.join(paths.get_save_slot_backup_dir(slot), backup_filename).replace("\\", "/")

        shutil.copy(get_game_save_path(slot), backup_filepath)

        viewport.window.evaluate_js('load_current_saves_list();')

    def update_last_mtime(self, slot: int):
        self.last_mtimes[slot] = os.path.getmtime(get_game_save_path(slot))


    # await py.exec(`import data.saves; retVal = data.saves.save_man.list_current_save_slots()`);
    def list_current_save_slots(self):
        current_save_folder = paths.get_game_save_dir()

        save_info = []

        for i in range(0, self.num_save_slots):
            newinfo = self.generate_save_file_info(os.path.join(current_save_folder, f"user_{i}.dat").replace("\\", "/"), True)
            if newinfo is not None:
                save_info.append(newinfo)

        # save_info.sort(key=lambda a: a['timestamp'], reverse=True)
        save_info.sort(key=lambda a: a['original_user'], reverse=False)

        self.latest_current_save_files = save_info

        return save_info

    def count_current_save_slots(self):
        current_save_folder = paths.get_game_save_dir()

        total = 0

        for i in range(0, self.num_save_slots):
            if os.path.isfile(os.path.join(current_save_folder, f"user_{i}.dat").replace("\\", "/"), True):
                total += 1

        return total

    def list_current_saves_found(self):
        current_save_folder = paths.get_game_save_dir()

        retVal = []

        for i in range(0, self.num_save_slots):
            if os.path.isfile(os.path.join(current_save_folder, f"user_{i}.dat").replace("\\", "/")):
                retVal.append(i)



        return retVal


    def list_backup_saves(self, slot: int):
        backup_save_folder = paths.get_save_slot_backup_dir(slot)

        save_info = []

        for i in os.listdir(backup_save_folder):
            newinfo = self.generate_save_file_info(os.path.join(backup_save_folder, i).replace("\\", "/"))
            if newinfo is not None:
                save_info.append(newinfo)


        save_info.sort(key=lambda a : a['timestamp'], reverse=True)

        self.latest_save_file_backups = save_info

        return save_info



    def generate_save_file_info(self, path: str, use_mtime: bool = False):
        # print(path)

        if not os.path.isfile(path):
            return

        filename = ntpath.basename(path)
        filename_noext = filename.split(".")[0]

        filename_list = filename_noext.split("_")


        stamp_source = 'mtime'
        use_timestamp = os.path.getmtime(path)
        if len(filename_list) < 2:
            return None
        elif len(filename_list) != 2 and not use_mtime:
            ts_str = filename_list[2].replace("-", ".")
            if ts_str.isdecimal():
                stamp_source = 'filename'
                use_timestamp = float(filename_list[2].replace("-", "."))


        return {
            'name': filename,
            'path': path,
            'type': filename_list[0],
            'original_user': int(filename_list[1]),
            'timestamp': use_timestamp,
            'timestamp_source': stamp_source,
            'datetime': str(datetime.datetime.fromtimestamp(float(use_timestamp))).split('.')[0],
            'size': os.path.getsize(path),
            'size_kb': int(os.path.getsize(path)/1000)
        }

    def load_past_save_file(self, slot: int, path: str):
        # Disallow save monitoring. We don't want it to detect it's own update to the save data.
        self.run_monitor = False
        file_info = self.generate_save_file_info(path)

        print(f"Reverting save slot {slot} to {file_info['name']} (Dated {datetime.datetime.fromtimestamp(file_info['timestamp'])})")
        shutil.copy(path, paths.get_game_save_slot_path(slot))

        print("Injecting reversion back into save history.")
        self.make_save_backup(slot, True)
        self.update_last_mtime(slot)
        self.run_monitor = True






save_man = SavesMan()