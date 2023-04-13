"""
For each element passed by the data mgr add a row and a button that if clicked run the linked exe file
"""
import os
import tkinter as tk
from typing import List
from lib.prog_exec_data_mgr import DataMgr, Prog, execute_prog
from functools import partial


class MainDlg():

    def __init__(self) -> None:
        self.window = None
        self.frm_main = None

    def _init_window(self) -> None:
        self.window = tk.Tk()
        self.window.resizable(False, False)

    def _click_on_settings_btn(self, event) -> None:
        print("settings :^)")

    def _init_footer(self) -> None:

        frm_footer = tk.Frame(bg="grey", padx=5, pady=5)

        btn_settings = tk.Button(relief=tk.RAISED,
                                 master=frm_footer,
                                 text="Settings",
                                 width=50,
                                 height=2,
                                 bg="black",
                                 fg="white",
                                 borderwidth=1,
                                 state='disabled')
        btn_settings.pack()
        btn_settings.bind("<Button-1>", self._click_on_settings_btn)

        frm_footer.pack(side=tk.BOTTOM, fill=tk.BOTH)

    def _click_on_prog_btn(self, exec_path: str):
        """
        """
        try:
            execute_prog(exec_path)
        except RuntimeError as err:
            print(str(err))
        else:
            self.window.destroy()

    def _add_programs_btns(self) -> List[Prog]:
        """
        """
        # search for the ini file
        ini_path = os.path.join(os.path.split(os.path.abspath(__file__))[0], "Programs.ini")
        if not os.path.isfile(ini_path):
            return []

        # try to create a data manager object
        try:
            self.config = DataMgr(ini_path)
        except Exception:
            return []

        # and try to create some buttons according to the data found
        programs_found = []
        for prog in self.config.get_programs():
            btn_tmp = tk.Button(relief=tk.RAISED,  # button style
                                master=self.frm_main,
                                text=prog.name,
                                width=50,
                                height=2,
                                bg="black",
                                fg="white",
                                borderwidth=1,
                                command=partial(self._click_on_prog_btn, prog.exec_path))  # click event
            # use partial otherwise the lambda is overwritten ^
            # link the button to the data obj
            prog.set_button(btn_tmp)

            # add to the list
            programs_found.append(prog)

        return programs_found

    def _init_main(self) -> None:
        """
        """
        self.frm_main = tk.Frame(relief=tk.RIDGE, bg="grey", padx=5, pady=5)
        btn_programs = self._add_programs_btns()

        for program in btn_programs:
            if program.button:
                program.button.pack()

        if not btn_programs:
            tk.Label(master=self.frm_main,
                     text="No programs configured yet ... :(",
                     bg="black",
                     fg="orange",
                     width=50,
                     height=10).pack()

        self.frm_main.pack(side=tk.TOP, fill=tk.BOTH)

    def run_dialog(self) -> None:
        # create the window
        self._init_window()

        # build the main body
        self._init_main()

        # build the window footer
        self._init_footer()

        # start catching the window's events
        self.window.mainloop()


if __name__ == "__main__":
    MainDlg().run_dialog()
