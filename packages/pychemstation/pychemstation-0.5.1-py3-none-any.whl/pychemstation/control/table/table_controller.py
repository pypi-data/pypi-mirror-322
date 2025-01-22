"""
Abstract module containing shared logic for Method and Sequence tables.

Authors: Lucy Hao
"""

import abc
import os
from typing import Union, Optional

import polling

from ...control import CommunicationController
from ...utils.chromatogram import AgilentHPLCChromatogram
from ...utils.macro import Command
from ...utils.method_types import MethodTimetable
from ...utils.sequence_types import SequenceDataFiles
from ...utils.table_types import Table, TableOperation, RegisterFlag


class TableController(abc.ABC):

    def __init__(self, controller: CommunicationController, src: str, data_dir: str):
        self.controller = controller
        if os.path.isdir(src):
            self.src: str = src
        else:
            raise FileNotFoundError(f"dir: {src} not found.")

        if os.path.isdir(data_dir):
            self.data_dir: str = data_dir
        else:
            raise FileNotFoundError(f"dir: {data_dir} not found.")

        self.spectra = {
            "A": AgilentHPLCChromatogram(self.data_dir),
            "B": AgilentHPLCChromatogram(self.data_dir),
            "C": AgilentHPLCChromatogram(self.data_dir),
            "D": AgilentHPLCChromatogram(self.data_dir),
        }

        self.data_files: Union[list[SequenceDataFiles], list[str]] = []

    def receive(self):
        return self.controller.receive()

    def send(self, cmd: Union[Command, str]):
        self.controller.send(cmd)

    def sleepy_send(self, cmd: Union[Command, str]):
        self.controller.sleepy_send(cmd)

    def sleep(self, seconds: int):
        """
        Tells the HPLC to wait for a specified number of seconds.

        :param seconds: number of seconds to wait
        """
        self.send(Command.SLEEP_CMD.value.format(seconds=seconds))

    def add_table_row(self, table: Table):
        """
        Adds a row to the provided table for currently loaded method or sequence.
        Import either the SEQUENCE_TABLE or METHOD_TIMETABLE from hein_analytical_control.constants.
        You can also provide your own table.

        :param table: the table to add a new row to
        """
        self.sleepy_send(TableOperation.NEW_ROW.value.format(register=table.register,
                                                             table_name=table.name))

    def delete_table(self, table: Table):
        """
        Deletes the table for the current loaded method or sequence.
        Import either the SEQUENCE_TABLE or METHOD_TIMETABLE from hein_analytical_control.constants.
        You can also provide your own table.

        :param table: the table to delete
        """
        self.sleepy_send(TableOperation.DELETE_TABLE.value.format(register=table.register,
                                                                  table_name=table.name))

    def new_table(self, table: Table):
        """
        Creates the table for the currently loaded method or sequence. Import either the SEQUENCE_TABLE or
        METHOD_TIMETABLE from hein_analytical_control.constants. You can also provide your own table.

        :param table: the table to create
        """
        self.send(TableOperation.CREATE_TABLE.value.format(register=table.register,
                                                           table_name=table.name))

    def _get_table_rows(self, table: Table) -> str:
        self.send(TableOperation.GET_OBJ_HDR_VAL.value.format(internal_val="Rows",
                                                              register=table.register,
                                                              table_name=table.name,
                                                              col_name=RegisterFlag.NUM_ROWS, ))
        res = self.controller.receive()
        self.send("Sleep 1")
        self.send('Print Rows')
        return res

    def check_hplc_ready_with_data(self, method: Optional[MethodTimetable] = None) -> bool:
        """
        Checks if ChemStation has finished writing data and can be read back.

        :param method: if you are running a method and want to read back data, the timeout period will be adjusted to be longer than the method's runtime
        :return: Return True if data can be read back, else False.
        """
        self.controller.set_status()

        timeout = 10 * 60
        hplc_run_done = polling.poll(
            lambda: self.controller.check_data(self.retrieve_recent_data_files()),
            timeout=timeout,
            step=30
        )

        return hplc_run_done

    @abc.abstractmethod
    def retrieve_recent_data_files(self):
        pass

    @abc.abstractmethod
    def get_data(self) -> tuple[bool,]:
        pass

    def get_spectrum(self, data_file: str):
        """
        Load chromatogram for any channel in spectra dictionary.
        """
        for channel, spec in self.spectra.items():
            spec.load_spectrum(data_path=data_file, channel=channel)

    def data_ready(self) -> bool:
        return self.check_hplc_ready_with_data()
