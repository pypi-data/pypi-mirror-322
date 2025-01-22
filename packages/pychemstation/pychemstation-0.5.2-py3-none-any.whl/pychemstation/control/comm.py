"""
Module to provide API for the communication with Agilent HPLC systems.

HPLCController sends commands to Chemstation software via a command file.
Answers are received via reply file. On the Chemstation side, a custom
Macro monitors the command file, executes commands and writes to the reply file.
Each command is given a number (cmd_no) to keep track of which commands have
been processed.

Authors: Alexander Hammer, Hessam Mehr, Lucy Hao
"""

import os
import time

from ..utils.constants import MAX_CMD_NO
from ..utils.macro import *
from ..utils.method_types import *


class CommunicationController:
    """
    Class that communicates with Agilent using Macros
    """

    def __init__(
            self,
            comm_dir: str,
            cmd_file: str = "cmd",
            reply_file: str = "reply",
    ):
        """
        :param comm_dir:
        :param cmd_file: Name of command file
        :param reply_file: Name of reply file
        """
        if os.path.isdir(comm_dir):
            self.cmd_file = os.path.join(comm_dir, cmd_file)
            self.reply_file = os.path.join(comm_dir, reply_file)
            self.cmd_no = 0
        else:
            raise FileNotFoundError(f"comm_dir: {comm_dir} not found.")
        self._most_recent_hplc_status = None

        # Create files for Chemstation to communicate with Python
        open(self.cmd_file, "a").close()
        open(self.reply_file, "a").close()

        self.reset_cmd_counter()

    def get_status(self) -> list[Union[HPLCRunningStatus, HPLCAvailStatus, HPLCErrorStatus]]:
        """Get device status(es).

        :return: list of ChemStation's current status
        """
        self.send(Command.GET_STATUS_CMD)
        time.sleep(1)

        try:
            parsed_response = self.receive().splitlines()[1].split()[1:]
            recieved_status = [str_to_status(res) for res in parsed_response]
            self._most_recent_hplc_status = recieved_status[0]
            return recieved_status
        except IOError:
            return [HPLCErrorStatus.NORESPONSE]
        except IndexError:
            return [HPLCErrorStatus.MALFORMED]

    def set_status(self):
        """Updates current status of HPLC machine"""
        self._most_recent_hplc_status = self.get_status()[0]

    def _check_data_status(self, data_path: str) -> bool:
        """Checks if HPLC machine is in an available state, meaning a state that data is not being written.

        :return: whether the HPLC machine is in a safe state to retrieve data back."""
        old_status = self._most_recent_hplc_status
        self.set_status()
        file_exists = os.path.exists(data_path)
        done_writing_data = isinstance(self._most_recent_hplc_status,
                                       HPLCAvailStatus) and old_status != self._most_recent_hplc_status and file_exists
        return done_writing_data

    def check_data(self, data_path: str) -> bool:
        return self._check_data_status(data_path)

    def _send(self, cmd: str, cmd_no: int, num_attempts=5) -> None:
        """Low-level execution primitive. Sends a command string to HPLC.

        :param cmd: string to be sent to HPLC
        :param cmd_no: Command number
        :param num_attempts: Number of attempts to send the command before raising exception.
        :raises IOError: Could not write to command file.
        """
        err = None
        for _ in range(num_attempts):
            time.sleep(1)
            try:
                with open(self.cmd_file, "w", encoding="utf8") as cmd_file:
                    cmd_file.write(f"{cmd_no} {cmd}")
            except IOError as e:
                err = e
                continue
            else:
                return
        else:
            raise IOError(f"Failed to send command #{cmd_no}: {cmd}.") from err

    def _receive(self, cmd_no: int, num_attempts=100) -> str:
        """Low-level execution primitive. Recives a response from HPLC.

        :param cmd_no: Command number
        :param num_attempts: Number of retries to open reply file
        :raises IOError: Could not read reply file.
        :return: ChemStation response 
        """
        err = None
        for _ in range(num_attempts):
            time.sleep(1)

            try:
                with open(self.reply_file, "r", encoding="utf_16") as reply_file:
                    response = reply_file.read()
            except OSError as e:
                err = e
                continue

            try:
                first_line = response.splitlines()[0]
                response_no = int(first_line.split()[0])
            except IndexError as e:
                err = e
                continue

            # check that response corresponds to sent command
            if response_no == cmd_no:
                return response
            else:
                continue
        else:
            raise IOError(f"Failed to receive reply to command #{cmd_no}.") from err

    def sleepy_send(self, cmd: Union[Command, str]):
        self.send("Sleep 0.1")
        self.send(cmd)
        self.send("Sleep 0.1")

    def send(self, cmd: Union[Command, str]):
        """Sends a command to Chemstation.

        :param cmd: Command to be sent to HPLC
        """
        if self.cmd_no == MAX_CMD_NO:
            self.reset_cmd_counter()

        cmd_to_send: str = cmd.value if isinstance(cmd, Command) else cmd
        self.cmd_no += 1
        self._send(cmd_to_send, self.cmd_no)

    def receive(self) -> str:
        """Returns messages received in reply file.

        :return: ChemStation response 
        """
        return self._receive(self.cmd_no)

    def reset_cmd_counter(self):
        """Resets the command counter."""
        self._send(Command.RESET_COUNTER_CMD.value, cmd_no=MAX_CMD_NO + 1)
        self._receive(cmd_no=MAX_CMD_NO + 1)
        self.cmd_no = 0

    def stop_macro(self):
        """Stops Macro execution. Connection will be lost."""
        self.send(Command.STOP_MACRO_CMD)
