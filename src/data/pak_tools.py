import os
import sys
import shutil
import threading
import multiprocessing
import multiprocessing.connection
import subprocess
import hashlib
import time
import settings.paths


class ToolMan:

    pak_proc: subprocess.Popen
    cdb_proc: subprocess.Popen

    # unpack_thread: threading.Thread
    unpack_mproc: multiprocessing.Process
    unpack_mproc_monitor_thread: threading.Thread

    def __init__(self):
        self.pak_name = "res.pak"
        self.cdb_name = "data.cdb"
        self.pak_proc = None
        self.cdb_proc = None

        # self.unpack_thread = None
        self.unpack_mproc = None
        self.unpack_mproc_monitor_thread = None

    # def get_main_cdb_path(self):
    #     return settings.paths.get_extract_res_dir() + "/" + self.cdb_name,

    def on_quit(self):
        if self.pak_proc is not None:
            self.pak_proc.kill()

        if self.cdb_proc is not None:
            self.cdb_proc.kill()

        if self.unpack_mproc is not None:
            self.unpack_mproc.kill()


    def get_extract_tree(self, current_dir = None):
        if current_dir is None:
            current_dir = settings.paths.get_extract_dir()

        dir_cont = os.listdir(current_dir)

        dir_dict = {
            'path': current_dir,
            'dirs': {},
            'files':{}

        }

        for i in dir_cont:
            fullpath = os.path.join(current_dir, i).replace("\\", "/")
            # print(fullpath)

            if os.path.isfile(fullpath):
                dir_dict['files'][i] = fullpath

            elif os.path.isdir(fullpath):
                dir_dict['dirs'][i] = self.get_extract_tree(fullpath)


        return dir_dict


    def get_main_pak_checksum(self):
        main_pak_file = open(settings.paths.get_main_pak(), 'rb')
        main_pak_data = main_pak_file.read()
        main_pak_file.close()

        # pipe contents of the file through
        return hashlib.md5(main_pak_data).hexdigest()

    def update_main_pak_checksum(self):
        settings.current['files']['main_pak_checksum'] = self.get_main_pak_checksum()

    # packing and unpacking:
    def is_any_running(self) -> bool:
        return (
            self.is_paktool_running()
            or self.is_cdbtool_running()
            or self.is_mproc_all_running()
        )

    def is_paktool_running(self) -> bool:
        return self.pak_proc is not None and self.pak_proc.poll() is None

    def run_extract_pak(self, filename: str = settings.paths.get_main_pak(), dest: str = settings.paths.get_extract_res_dir()) -> subprocess.Popen:
        # if filename is None:
            # filename = settings.paths.get_main_pak()
            # filename = self.pak_name

        if self.is_paktool_running():
            print("Killing last unpacking process...")
            self.pak_proc.kill()

        self.pak_proc = subprocess.Popen(
            [
                settings.paths.get_pak_tool(),
                "-Expand",
                "-outdir",
                dest,
                # settings.paths.get_extract_res_dir(),
                "-refpak",
                filename,
            ],
            cwd=os.getcwd(),
            stdout=subprocess.PIPE
        )
        return self.pak_proc

    def run_rebuild_pak(self, filename: str = settings.paths.get_main_pak(), src: str = settings.paths.get_extract_res_dir()) -> subprocess.Popen:
        # if filename is None:
        #     filename = self.pak_name

        if self.is_paktool_running():
            print("Killing last unpacking process...")
            self.pak_proc.kill()

        self.pak_proc = subprocess.Popen(
            [
                settings.paths.get_pak_tool(),
                "-Collapse",
                "-indir",
                src,
                "-outpak",
                filename,
            ],
            cwd=os.getcwd(),
        )
        return self.pak_proc

    # def is_extracting_cdb(self) -> bool:
    def is_cdbtool_running(self) -> bool:
        return self.cdb_proc is not None and self.cdb_proc.poll() is None

    def run_extract_cdb(self, src: str = settings.paths.get_main_cdb(), dst: str = settings.paths.get_extract_cdb_dir()) -> subprocess.Popen:
        if self.is_cdbtool_running():
            print("Killing last cdbtool process...")
            self.cdb_proc.kill()

        self.cdb_proc = subprocess.Popen(
            [
                settings.paths.get_cdb_tool(),
                "-Expand",
                "-outdir",
                dst,
                "-refcdb",
                src,
            ],
            cwd=os.getcwd(),
            stdout=subprocess.PIPE
        )
        return self.cdb_proc

    def run_rebuild_cdb(self, src: str = settings.paths.get_extract_cdb_dir(), dst: str = settings.paths.get_main_cdb()) -> subprocess.Popen:
        if self.is_cdbtool_running():
            print("Killing last cdbtool process...")
            self.cdb_proc.kill()

        self.cdb_proc = subprocess.Popen(
            [
                settings.paths.get_cdb_tool(),
                "-collapse",
                "-indir",
                src,
                "-outcdb",
                dst,
            ],
            cwd=os.getcwd(),
        )
        return self.cdb_proc

    def is_mproc_all_running(self):
        return self.unpack_mproc is not None and self.unpack_mproc.is_alive()

    def run_unpack_all(self, filename: str = None):
        self.unpack_mproc_monitor_thread = None
        if filename is None:
            filename = settings.paths.get_main_pak()
            # filename = self.pak_name

        if self.is_mproc_all_running():
            print("Previous mproc in progress. Please wait.")
            return

        # self.unpack_mproc = multiprocessing.Process(group=None, target=unpack_process, args=(self.pak_name, self.cdb_name))

        parent_pipe, child_pipe = multiprocessing.Pipe()
        self.unpack_mproc = multiprocessing.Process(
            group=None, target=unpack_process, args=tuple([self, filename, child_pipe])
        )
        self.unpack_mproc.start()

        self.unpack_mproc_monitor_thread = threading.Thread(None, self.monitor_mproc, args=(self.unpack_mproc, parent_pipe))
        self.unpack_mproc_monitor_thread.start()
        return self.unpack_mproc

    def run_rebuild_all(self, filename: str = None):
        self.unpack_mproc_monitor_thread = None
        if filename is None:
            filename = settings.paths.get_main_pak()
            # filename = self.pak_name

        if self.is_mproc_all_running():
            print("Previous mproc in progress. Please wait.")
            return

        # self.unpack_mproc = multiprocessing.Process(group=None, target=unpack_process, args=(self.pak_name, self.cdb_name))

        parent_pipe, child_pipe = multiprocessing.Pipe()
        self.unpack_mproc = multiprocessing.Process(
            group=None, target=repack_process, args=tuple([self, filename, child_pipe])
        )
        self.unpack_mproc.start()
        self.unpack_mproc_monitor_thread = threading.Thread(None, self.monitor_mproc, args=(self.unpack_mproc, parent_pipe))
        self.unpack_mproc_monitor_thread.start()
        return self.unpack_mproc

    def monitor_mproc(self, proc: multiprocessing.Process, pipe: multiprocessing.connection.Connection):
        piped_message = ""
        while piped_message != "Done" and proc.is_alive() and not pipe.closed:
            piped_message = pipe.recv()
            print("PIPED THROUGH: " + str(piped_message))

        print("Updating Checksum...")
        tool_man.update_main_pak_checksum()
        print("Checksum updated.")
        pipe.close()
        self.unpack_mproc_monitor_thread = None






def unpack_process(p_tool_man: ToolMan, filename: str, pipe: multiprocessing.connection.Connection):
    # sys.stdout = open(str(os.getpid()) + ".out", 'w')
    def smart_print(x):
        print(x)
        pipe.send(x)
        sys.stdout.flush()

    smart_print("Unpacking res.pak")
    proc1 = p_tool_man.run_extract_pak(filename)

    while proc1.poll() is None:
        smart_print(proc1.communicate())


    smart_print("Expanding data.cdb")
    proc2 = p_tool_man.run_extract_cdb()
    while proc2.poll() is None:
        smart_print(proc2.communicate())



    smart_print("Done")
    pipe.close()

def repack_process(p_tool_man: ToolMan, filename: str, pipe: multiprocessing.connection.Connection):
    # sys.stdout = open(str(os.getpid()) + ".out", 'w')
    def smart_print(x):
        print(x)
        pipe.send(x)
        sys.stdout.flush()

    smart_print("Rebuilding CastleDB")
    proc1 = p_tool_man.run_rebuild_cdb()

    while proc1.poll() is None:
        smart_print(proc1.communicate())

    smart_print("Rebuilding res.pak")
    proc2 = p_tool_man.run_rebuild_pak(filename)
    while proc2.poll() is None:
        smart_print(proc2.communicate())

    smart_print("Done")
    pipe.close()


tool_man = ToolMan()