from typing import Any

from copy import deepcopy

import os
import time

from .table_controller import TableController
from ...control import CommunicationController
from ...utils.chromatogram import SEQUENCE_TIME_FORMAT, AgilentHPLCChromatogram
from ...utils.constants import SEQUENCE_TABLE
from ...utils.macro import Command
from ...utils.sequence_types import SequenceTable, SequenceEntry, SequenceDataFiles
from ...utils.table_types import TableOperation, RegisterFlag


class SequenceController(TableController):
    """
    Class containing sequence related logic
    """

    def __init__(self, controller: CommunicationController, src: str, data_dir: str):
        super().__init__(controller, src, data_dir)

    def switch(self, seq_name: str):
        """
        Switch to the specified sequence. The sequence name does not need the '.S' extension.

        :param seq_name: The name of the sequence file
        """
        self.send(f'_SeqFile$ = "{seq_name}.S"')
        self.send(f'_SeqPath$ = "{self.src}"')
        self.send(Command.SWITCH_SEQUENCE_CMD)
        time.sleep(2)
        self.send(Command.GET_SEQUENCE_CMD)
        time.sleep(2)
        # check that method switched
        for _ in range(10):
            try:
                parsed_response = self.receive().splitlines()[1].split()[1:][0]
                break
            except IndexError:
                continue

        assert parsed_response == f"{seq_name}.S", "Switching sequence failed."

    def edit(self, sequence_table: SequenceTable):
        """
        Updates the currently loaded sequence table with the provided table. This method will delete the existing sequence table and remake it.
        If you would only like to edit a single row of a sequence table, use `edit_sequence_table_row` instead.

        :param sequence_table:
        """
        self.send("Local Rows")
        self.sleep(1)
        self.delete_table(SEQUENCE_TABLE)
        self.sleep(1)
        self.new_table(SEQUENCE_TABLE)
        self.sleep(1)
        self._get_table_rows(SEQUENCE_TABLE)

        for _ in sequence_table.rows:
            self.add_table_row(SEQUENCE_TABLE)
            self.sleep(1)
            self.send(Command.SAVE_SEQUENCE_CMD)
        self._get_table_rows(SEQUENCE_TABLE)
        self.send(Command.SAVE_SEQUENCE_CMD)
        self.send(Command.SWITCH_SEQUENCE_CMD)

        for i, row in enumerate(sequence_table.rows):
            self.edit_row(row=row, row_num=i + 1)
            self.sleep(1)
        self.send(Command.SAVE_SEQUENCE_CMD)


    def edit_row(self, row: SequenceEntry, row_num: int):
        """
        Edits a row in the sequence table. Assumes the row already exists.

        :param row: sequence row entry with updated information
        :param row_num: the row to edit, based on -1-based indexing
        """
        if row.vial_location:
            self.sleepy_send(TableOperation.EDIT_ROW_VAL.value.format(register=SEQUENCE_TABLE.register,
                                                                      table_name=SEQUENCE_TABLE.name,
                                                                      row=row_num,
                                                                      col_name=RegisterFlag.VIAL_LOCATION,
                                                                      val=row.vial_location))
        if row.method:
            self.sleepy_send(TableOperation.EDIT_ROW_TEXT.value.format(register=SEQUENCE_TABLE.register,
                                                                       table_name=SEQUENCE_TABLE.name,
                                                                       row=row_num,
                                                                       col_name=RegisterFlag.METHOD,
                                                                       val=row.method))

        if row.num_inj:
            self.sleepy_send(TableOperation.EDIT_ROW_VAL.value.format(register=SEQUENCE_TABLE.register,
                                                                      table_name=SEQUENCE_TABLE.name,
                                                                      row=row_num,
                                                                      col_name=RegisterFlag.NUM_INJ,
                                                                      val=row.num_inj))

        if row.inj_vol:
            self.sleepy_send(TableOperation.EDIT_ROW_TEXT.value.format(register=SEQUENCE_TABLE.register,
                                                                       table_name=SEQUENCE_TABLE.name,
                                                                       row=row_num,
                                                                       col_name=RegisterFlag.INJ_VOL,
                                                                       val=row.inj_vol))

        if row.inj_source:
            self.sleepy_send(TableOperation.EDIT_ROW_TEXT.value.format(register=SEQUENCE_TABLE.register,
                                                                       table_name=SEQUENCE_TABLE.name,
                                                                       row=row_num,
                                                                       col_name=RegisterFlag.INJ_SOR,
                                                                       val=row.inj_source.value))

        if row.sample_name:
            self.sleepy_send(TableOperation.EDIT_ROW_TEXT.value.format(register=SEQUENCE_TABLE.register,
                                                                       table_name=SEQUENCE_TABLE.name,
                                                                       row=row_num,
                                                                       col_name=RegisterFlag.NAME,
                                                                       val=row.sample_name))
            self.sleepy_send(TableOperation.EDIT_ROW_TEXT.value.format(register=SEQUENCE_TABLE.register,
                                                                       table_name=SEQUENCE_TABLE.name,
                                                                       row=row_num,
                                                                       col_name=RegisterFlag.DATA_FILE,
                                                                       val=row.sample_name))
        if row.sample_type:
            self.sleepy_send(TableOperation.EDIT_ROW_VAL.value.format(register=SEQUENCE_TABLE.register,
                                                                      table_name=SEQUENCE_TABLE.name,
                                                                      row=row_num,
                                                                      col_name=RegisterFlag.SAMPLE_TYPE,
                                                                      val=row.sample_type.value))

    def run(self, sequence_table: SequenceTable):
        """
        Starts the currently loaded sequence, storing data
        under the <data_dir>/<sequence table name> folder.
        Device must be ready.

        :param sequence_table:
        """
        timestamp = time.strftime(SEQUENCE_TIME_FORMAT)
        self.send(Command.RUN_SEQUENCE_CMD.value)
        folder_name = f"{sequence_table.name} {timestamp}"
        subdirs = [x[0] for x in os.walk(self.data_dir)]
        time.sleep(10)
        potential_folders = sorted(list(filter(lambda d: folder_name in d, subdirs)))
        parent_folder = potential_folders[0]
        self.data_files.append(SequenceDataFiles(
            sequence_name=sequence_table.name,
            dir=parent_folder,
            child_dirs=[r.sample_name + ".D" for r in sequence_table.rows]))

    def retrieve_recent_data_files(self):
        sequence_data_files: SequenceDataFiles = self.data_files[-1]
        return os.path.join(sequence_data_files.dir, sequence_data_files.child_dirs[-1])

    def get_data(self) -> tuple[bool, Any]:
        data_ready = self.data_ready()
        sequence_data_files: SequenceDataFiles = self.data_files[-1]
        spectra: list[dict[str, AgilentHPLCChromatogram]] = []
        if data_ready:
            for row in sequence_data_files.child_dirs:
                data_path = os.path.join(sequence_data_files.dir, row)
                self.get_spectrum(data_path)
                spectra.append(deepcopy(self.spectra))
            return data_ready, spectra
        else:
            return False, None
