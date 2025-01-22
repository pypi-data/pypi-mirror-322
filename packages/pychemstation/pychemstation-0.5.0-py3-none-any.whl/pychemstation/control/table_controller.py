import os
from typing import Union


from .comm import HPLCController
from ..utils.macro import Command
from ..utils.table_types import Table, TableOperation, RegisterFlag


class TableController:

    def __init__(self, controller: HPLCController, src: str):
        self.controller = controller
        if os.path.isdir(src):
            self.src: str = src
        else:
            raise FileNotFoundError(f"dir: {src} not found.")

    def sleep(self, seconds: int):
        self.controller.sleep(seconds)

    def receive(self):
        self.controller.receive()

    def send(self, cmd: Union[Command, str]):
        self.controller.send(cmd)

    def sleepy_send(self, cmd: Union[Command, str]):
        self.controller.sleepy_send(cmd)

    def add_table_row(self, table: Table):
        """Adds a row to the provided table for currently loaded method or sequence.
         Import either the SEQUENCE_TABLE or METHOD_TIMETABLE from hein_analytical_control.constants.
        You can also provide your own table.

        :param table: the table to add a new row to
        """
        self.sleepy_send(TableOperation.NEW_ROW.value.format(register=table.register,
                                                             table_name=table.name))

    def delete_table(self, table: Table):
        """Deletes the table for the current loaded method or sequence.
         Import either the SEQUENCE_TABLE or METHOD_TIMETABLE from hein_analytical_control.constants.
        You can also provide your own table.

        :param table: the table to delete
        """
        self.sleepy_send(TableOperation.DELETE_TABLE.value.format(register=table.register,
                                                                  table_name=table.name))

    def new_table(self, table: Table):
        """Creates the table for the currently loaded method or sequence. Import either the SEQUENCE_TABLE or
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

    def get_data(self):
        self.controller.get_spectrum()
        return self.controller.spectra["A"]

    def data_ready(self) -> bool:
        return self.controller.check_hplc_ready_with_data()
