"""
Read the ini file and return the data structure
"""
import os
import configparser
from threading import Thread
from subprocess import Popen as run_cmd
from tkinter import Button
from typing import List


def _execute_prog(prog_exe_path: str) -> None:
    run_cmd([prog_exe_path])


def execute_prog(prog_exe_path: str) -> None:
    if not os.path.isfile(prog_exe_path):
        raise RuntimeError("Not a real file")

    # start in a new thread and allow to end the run even if the thread hasn't finished
    Thread(target=_execute_prog, args=([prog_exe_path]), daemon=False).start()

    # sys.exit(0) # this shouldn't be needed anymore thanks to 'daemon=True' ^


class Prog():
    def __init__(self, name: str, exec_path: str) -> None:
        self.name = name
        self.exec_path = exec_path
        self.button = None

    def set_button(self, button: Button) -> None:
        self.button = button


class ConfigSettings():

    config_dict = None

    def __init__(self, ini_path: str):
        if not os.path.isdir(os.path.split(ini_path)[0]):
            os.makedirs(os.path.split(ini_path)[0])

        self._ini_path = ini_path

        self.config_dict = self._get_config()

    def _get_config(self):
        cfgfile = configparser.ConfigParser(allow_no_value=True)
        # reading the customer's ini file
        cfgfile.read(self._ini_path)
        return cfgfile


class DataMgr(ConfigSettings):

    def __init__(self, ini_path) -> None:
        super().__init__(ini_path)

    def get_programs(self) -> List[Prog]:
        prog_list = []
        for section, data in self.config_dict.items():

            # skip the default (not a real field)
            if section.upper() == "DEFAULT":
                continue

            # store the 'ExecPath' field if found
            try:
                exec_path = data["ExecPath"]
            except Exception:
                exec_path = ""

            prog_list.append(Prog(section, exec_path))

        return prog_list
