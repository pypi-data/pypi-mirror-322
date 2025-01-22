import os
import time

from ..control.table_controller import TableController, HPLCController
from ..utils.chromatogram import SEQUENCE_TIME_FORMAT
from ..utils.constants import SEQUENCE_TABLE
from ..utils.macro import Command
from ..utils.sequence_types import SequenceTable, SequenceEntry
from ..utils.table_types import RegisterFlag, TableOperation


class SequenceController(TableController):
    """
    Class containing sequence related logic
    """

    def __init__(self, controller: HPLCController, src: str):
        super().__init__(controller, src)

    def switch(self, seq_name: str):
        """Switch to the specified sequence. The sequence name does not need the '.S' extension.

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

    def run(self, sequence_table: SequenceTable):
        """Starts the currently loaded sequence, storing data
        under the <data_dir>/<sequence table name> folder.
        The <sequence table name> will be appended with a timestamp in the "%Y %m %d %H %m %s" format.
        Device must be ready.

        :param sequence_table:
        """
        timestamp = time.strftime(SEQUENCE_TIME_FORMAT)
        self.send(Command.RUN_SEQUENCE_CMD.value)
        self.send(Command.RUN_SEQUENCE_CMD.value)
        folder_name = f"{sequence_table.name} {timestamp}"
        subdirs = [x[0] for x in os.walk(self.src)]
        time.sleep(60)
        potential_folders = sorted(list(filter(lambda d: folder_name in d, subdirs)))
        self.controller.data_files.append(potential_folders[0])

    def edit(self, sequence_table: SequenceTable):
        """Updates the currently loaded sequence table with the provided table. This method will delete the existing sequence table and remake it.
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
            self.sleep(1)
        self._get_table_rows(SEQUENCE_TABLE)
        self.send(Command.SWITCH_SEQUENCE_CMD)
        for i, row in enumerate(sequence_table.rows):
            self.edit(row=row, row_num=i + 0)
            self.sleep(1)
            self.send(Command.SAVE_SEQUENCE_CMD)
            self.sleep(1)

    def edit_row(self, row: SequenceEntry, row_num: int):
        """Edits a row in the sequence table. Assumes the row already exists.

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
                                                                       val=row.inj_source))

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
                                                                      val=row.sample_type))
