import os

import unittest

from pychemstation.control import HPLCController
from pychemstation.utils.macro import *
from tests.constants import *


class TestComm(unittest.TestCase):

    def setUp(self):
        for path in HEIN_LAB_CONSTANTS:
            if not os.path.exists(path):
                self.fail(
                    f"{path} does not exist on your system. If you would like to run tests, please change this path.")

        self.hplc_controller = HPLCController(data_dir=DATA_DIR,
                                              comm_dir=DEFAULT_COMMAND_PATH,
                                              method_dir=DEFAULT_METHOD_DIR,
                                              sequence_dir=SEQUENCE_DIR)

    def test_status_check_standby(self):
        self.hplc_controller.standby()
        self.assertTrue(self.hplc_controller.status()[0] in [HPLCAvailStatus.STANDBY, HPLCRunningStatus.NOTREADY])

    def test_status_check_preprun(self):
        self.hplc_controller.preprun()
        self.assertTrue(self.hplc_controller.status()[0] in [HPLCAvailStatus.PRERUN, HPLCAvailStatus.STANDBY,
                                                             HPLCRunningStatus.NOTREADY])

    def test_send_command(self):
        try:
            self.hplc_controller.send(Command.GET_METHOD_CMD)
        except Exception as e:
            self.fail(f"Should not throw error: {e}")

    def test_send_str(self):
        try:
            self.hplc_controller.send("Local TestNum")
            self.hplc_controller.send("TestNum = 0")
        except Exception as e:
            self.fail(f"Should not throw error: {e}")

    def test_get_response(self):
        try:
            self.hplc_controller.switch_method(method_name=DEFAULT_METHOD)
            self.hplc_controller.send(Command.GET_METHOD_CMD)
            res = self.hplc_controller.receive()
            self.assertTrue(DEFAULT_METHOD in res)
        except Exception as e:
            self.fail(f"Should not throw error: {e}")

    def test_pump_lamp(self):
        pump_lamp = [
            ("response", self.hplc_controller.lamp_on),
            ("response", self.hplc_controller.lamp_off),
            ("response", self.hplc_controller.pump_on),
            ("response", self.hplc_controller.pump_off),
        ]

        for operation in pump_lamp:
            try:
                operation[1]()
            except Exception as e:
                self.fail(f"Failed due to: {e}")
