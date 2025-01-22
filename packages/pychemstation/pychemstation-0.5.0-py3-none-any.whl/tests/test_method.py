import os
import unittest

from pychemstation.control import HPLCController
from pychemstation.utils.method_types import *
from tests.constants import *


class TestMethod(unittest.TestCase):
    def setUp(self):
        for path in HEIN_LAB_CONSTANTS:
            if not os.path.exists(path):
                self.fail(
                    f"{path} does not exist on your system. If you would like to run tests, please change this path.")

        self.hplc_controller = HPLCController(data_dir=DATA_DIR,
                                              comm_dir=DEFAULT_COMMAND_PATH,
                                              method_dir=DEFAULT_METHOD_DIR,
                                              sequence_dir=SEQUENCE_DIR)



    def test_load_method_details(self):
        self.hplc_controller.switch_method(DEFAULT_METHOD)
        try:
            gp_mtd = self.hplc_controller.method_controller.load(DEFAULT_METHOD)
            self.assertTrue(gp_mtd.first_row.organic_modifier.val == 5)
        except Exception as e:
            self.fail(f"Should have not failed, {e}")

    def test_method_update_timetable(self):
        self.hplc_controller.method_controller.switch(DEFAULT_METHOD)
        new_method = MethodTimetable(
            first_row=HPLCMethodParams(
                organic_modifier=7,
                flow=0.44,
                maximum_run_time=2,
                temperature=15),
            subsequent_rows=[
                TimeTableEntry(
                    start_time=0.10,
                    organic_modifer=7,
                    flow=0.34),
                TimeTableEntry(
                    start_time=1,
                    organic_modifer=99,
                    flow=0.55)])
        try:
            self.hplc_controller.edit_method(new_method)
        except Exception as e:
            self.fail(f"Should have not failed: {e}")

    def test_run_method(self):
        try:
            self.hplc_controller.run_method(experiment_name="test_experiment")
            chrom = self.hplc_controller.get_last_run_method_data()
        except Exception as e:
            self.fail(f"Should have not failed: {e}")




if __name__ == '__main__':
    unittest.main()
