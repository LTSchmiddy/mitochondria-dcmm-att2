from __future__ import annotations

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

    custom_name: str

    def __init__(self):
        self.filepath = None
        self.custom_name = ""

    @staticmethod
    def load_from_path(path: str) -> SaveBackup:
        if not os.path.isfile(path):
            return None

        loaded_backup: SaveBackup = pickle.load(open(path, 'rb'))
        loaded_backup.filepath = path
        loaded_backup.file_timestamp = os.path.getmtime(path)

        return loaded_backup

    @staticmethod
    def make_from_game_save(original_slot: int) -> SaveBackup:
        game_save_path = paths.get_game_save_path(original_slot)

        if not os.path.isfile(game_save_path):
            return None

        new_backup = SaveBackup()

        # getting file metadata:
        new_backup.update_file_timestamp()

        new_backup.original_timestamp = os.path.getmtime(game_save_path)
        new_backup.original_user = original_slot
        new_backup.save_type = SaveType.game_save

        # getting savedata:
        new_backup.record_game_save()
        new_backup.save_to_disk()



    @property
    def filename(self) -> str:
        return ntpath.basename(self.filepath)

    @property
    def sorting_timestamp(self) -> float:
        if self.save_type == SaveType.injected_save:
            return self.file_timestamp

        return self.original_timestamp

    @property
    def original_datetime(self) -> datetime.datetime:
        return datetime.datetime.fromtimestamp(self.original_timestamp)

    @property
    def original_datetime_str(self) -> str:
        return str(datetime.datetime.fromtimestamp(self.original_timestamp))

    @property
    def file_datetime(self) -> datetime.datetime:
        return datetime.datetime.fromtimestamp(self.file_timestamp)

    @property
    def file_datetime_str(self) -> str:
        return str(datetime.datetime.fromtimestamp(self.file_timestamp))

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

    def update_file_timestamp(self):
        self.file_timestamp = datetime.datetime.now().timestamp()

    def generate_file_name(self, set_filepath: bool = False):
        retVal = ""
        if self.save_type == SaveType.game_save:
            retVal = f"""user_{self.original_user}_{str(self.original_timestamp).replace(".", "-")}.mdcs"""

        else:
            retVal = f"""injected_{self.original_user}_{str(self.file_timestamp).replace(".", "-")}.mdcs"""

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

    def record_game_save(self, slot: int = None):
        if slot is None:
            slot = self.original_user

        game_save_file = open(paths.get_game_save_path(slot), 'rb')
        self.save_data = game_save_file.read()
        game_save_file.close()

    def inject_into_game_save(self, slot: int = None, do_post_injection: bool = True, save_injection_to_disk: bool = False):
        if slot is None:
            slot = self.original_user

        outfile = open(paths.get_game_save_path(slot), 'wb')
        outfile.write(self.save_data)
        outfile.close()

        if do_post_injection:
            self.save_type = SaveType.injected_save
            self.update_file_timestamp()
            self.generate_file_name(True)

            if save_injection_to_disk:
                self.save_to_disk()


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

        if not os.path.isfile(paths.get_game_save_path(slot)):
            return

        if len(os.listdir(paths.get_save_slot_backup_dir(slot))) == 0:
            self.make_save_backup(slot)
        else:
            if self.last_mtimes[slot] == 0:
                self.last_mtimes[slot] = self.list_backup_saves(slot)[0].file_timestamp

        if os.path.getmtime(paths.get_game_save_path(slot)) > self.last_mtimes[slot]:
            self.make_save_backup(slot)
            print(f"Save slot {slot} updated. Backing up...")
            self.update_last_mtime(slot)


    def make_save_backup(self, slot: int, is_injected: bool = False):
        SaveBackup.make_from_game_save(slot)
        self.update_last_mtime(slot)

        viewport.window.evaluate_js('load_current_saves_list();')


    def update_last_mtime(self, slot: int):
        self.last_mtimes[slot] = os.path.getmtime(paths.get_game_save_path(slot))


    # await py.exec(`import data.saves; retVal = data.saves.save_man.list_current_save_slots()`);
    def list_current_save_slots(self):
        current_save_folder = paths.get_game_save_dir()

        save_info = []

        for i in range(0, self.num_save_slots):
            newinfo = self.generate_game_save_file_info(os.path.join(current_save_folder, f"user_{i}.dat").replace("\\", "/"), True)
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

    def generate_game_save_file_info(self, path: str, use_mtime: bool = False):
        # print(path)

        if not os.path.isfile(path):
            return

        filename = ntpath.basename(path)
        filename_noext = filename.split(".")[0]

        filename_list = filename_noext.split("_")

        use_timestamp = os.path.getmtime(path)
        return {
            'name': filename,
            'path': path,
            'type': filename_list[0],
            'original_user': int(filename_list[1]),
            'timestamp': use_timestamp,
            'datetime': str(datetime.datetime.fromtimestamp(float(use_timestamp))).split('.')[0],
            'size': os.path.getsize(path),
            'size_kb': int(os.path.getsize(path)/1000)
        }

    def list_current_saves_found(self):
        current_save_folder = paths.get_game_save_dir()

        retVal = []

        for i in range(0, self.num_save_slots):
            if os.path.isfile(os.path.join(current_save_folder, f"user_{i}.dat").replace("\\", "/")):
                retVal.append(i)

        return retVal


    def list_backup_saves(self, slot: int, how_many: int = None):
        backup_save_folder = paths.get_save_slot_backup_dir(slot)

        save_info = []

        for i in os.listdir(backup_save_folder):
            newbackup = SaveBackup.load_from_path(os.path.join(backup_save_folder, i).replace("\\", "/"))
            if newbackup is not None:
                save_info.append(newbackup)


        save_info.sort(key=lambda a : a.sorting_timestamp, reverse=True)

        self.latest_save_file_backups = save_info

        if how_many is None or len(save_info) <= how_many:
            return save_info

        return save_info [:how_many]

    def count_backup_saves(self, slot: int):
        backup_save_folder = paths.get_save_slot_backup_dir(slot)

        total = 0

        for i in os.listdir(backup_save_folder):
            newbackup = SaveBackup.load_from_path(os.path.join(backup_save_folder, i).replace("\\", "/"))
            if newbackup is not None:
                total += 1


        return total


    def load_past_save_file(self, slot: int, path: str):
        # Disallow save monitoring. We don't want it to detect it's own update to the save data.
        self.run_monitor = False
        file_info = SaveBackup.load_from_path(path)

        print(f"Reverting save slot {slot} to {file_info.filename} (Dated {datetime.datetime.fromtimestamp(file_info.original_timestamp)}")
        file_info.inject_into_game_save(slot, True, True)

        print("Injecting reversion back into save history.")
        self.update_last_mtime(slot)
        self.run_monitor = True

        viewport.window.evaluate_js('load_current_saves_list();')





save_man = SavesMan()