import os
import unittest

from pychemstation.control import HPLCController
from pychemstation.utils.sequence_types import *
from tests.constants import *


class TestSequence(unittest.TestCase):
    def setUp(self):
        for path in HEIN_LAB_CONSTANTS:
            if not os.path.exists(path):
                self.fail(
                    f"{path} does not exist on your system. If you would like to run tests, please change this path.")

        self.hplc_controller = HPLCController(data_dir=DATA_DIR,
                                              comm_dir=DEFAULT_COMMAND_PATH,
                                              method_dir=DEFAULT_METHOD_DIR,
                                              sequence_dir=SEQUENCE_DIR)

    def test_switch(self):
        try:
            self.hplc_controller.switch_sequence(sequence_name=DEFAULT_SEQUENCE)
        except Exception as e:
            self.fail(f"Should have not expected: {e}")

    def test_edit_row(self):
        self.hplc_controller.switch_sequence(sequence_name=DEFAULT_SEQUENCE)
        self.hplc_controller.edit_sequence_row(SequenceEntry(
                    vial_location=10,
                    method="C:\\ChemStation\\1\\Methods\\General-Poroshell",
                    num_inj=3,
                    inj_vol=4,
                    sample_name="Blank",
                    sample_type=SampleType.BLANK,
                    inj_source=InjectionSource.HIP_ALS
                ), 1)

    def test_edit_entire_table(self):
        self.hplc_controller.switch_sequence(sequence_name=DEFAULT_SEQUENCE)
        seq_table = SequenceTable(
            name=DEFAULT_SEQUENCE,
            rows=[
                SequenceEntry(
                    vial_location=3,
                    method="C:\\ChemStation\\1\\Methods\\General-Poroshell",
                    num_inj=3,
                    inj_vol=4,
                    sample_name="Control",
                    sample_type=SampleType.CONTROL,
                    inj_source=InjectionSource.MANUAL
                ),
                SequenceEntry(
                    vial_location=1,
                    method="C:\\ChemStation\\1\\Methods\\General-Poroshell",
                    num_inj=1,
                    inj_vol=1,
                    sample_name="Sample",
                    sample_type=SampleType.SAMPLE,
                    inj_source=InjectionSource.AS_METHOD
                ),
                SequenceEntry(
                    vial_location=10,
                    method="C:\\ChemStation\\1\\Methods\\General-Poroshell",
                    num_inj=3,
                    inj_vol=4,
                    sample_name="Blank",
                    sample_type=SampleType.BLANK,
                    inj_source=InjectionSource.HIP_ALS
                ),
            ]
        )
        self.hplc_controller.edit_sequence(seq_table)


    def test_run(self):
        # self.hplc_controller.switch_sequence(sequence_name=DEFAULT_SEQUENCE)
        seq_table = SequenceTable(
            name=DEFAULT_SEQUENCE,
            rows=[
                SequenceEntry(
                    vial_location=1,
                    method="C:\\ChemStation\\1\\Methods\\" + DEFAULT_METHOD,
                    num_inj=1,
                    inj_vol=1,
                    sample_name="Test",
                    sample_type=SampleType.BLANK
                ),
                SequenceEntry(
                    vial_location=2,
                    method="C:\\ChemStation\\1\\Methods\\" + DEFAULT_METHOD,
                    num_inj=1,
                    inj_vol=1,
                    sample_name="Test2",
                    sample_type=SampleType.BLANK
                ),
            ]
        )
        self.hplc_controller.edit_sequence(seq_table)
        self.hplc_controller.run_sequence(seq_table)
        chrom = self.hplc_controller.get_last_run_sequence_data()
        self.assertTrue(len(chrom) == 2)
