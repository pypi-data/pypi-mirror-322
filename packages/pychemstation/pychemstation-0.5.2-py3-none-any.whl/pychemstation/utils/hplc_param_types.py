from dataclasses import dataclass
from enum import Enum
from typing import Union, Any, Optional

from pychemstation.generated import SolventElement, Signal


# Commands sent to the Chemstation Macro
# See https://www.agilent.com/cs/library/usermanuals/Public/MACROS.PDF
class Command(Enum):
    def __str__(self):
        return '%s' % self.value

    RESET_COUNTER_CMD = "last_cmd_no = 0"
    GET_STATUS_CMD = "response$ = AcqStatus$"
    SLEEP_CMD = "Sleep {seconds}"
    STANDBY_CMD = "Standby"
    STOP_MACRO_CMD = "Stop"
    PREPRUN_CMD = "PrepRun"
    LAMP_ON_CMD = "LampAll ON"
    LAMP_OFF_CMD = "LampAll OFF"
    PUMP_ON_CMD = "PumpAll ON"
    PUMP_OFF_CMD = "PumpAll OFF"
    GET_METHOD_CMD = "response$ = _MethFile$"
    SWITCH_METHOD_CMD = 'LoadMethod "{method_dir}", "{method_name}.M"'
    START_METHOD_CMD = "StartMethod"
    RUN_METHOD_CMD = 'RunMethod "{data_dir}",, "{experiment_name}_{timestamp}"'
    STOP_METHOD_CMD = "StopMethod"
    UPDATE_METHOD_CMD = 'UpdateMethod'
    SWITCH_SEQUENCE_CMD = 'LoadSequence _SeqPath$, _SeqFile$'
    SAVE_SEQUENCE_CMD = 'SaveSequence _SeqPath$, _SeqFile$'
    GET_SEQUENCE_CMD = 'response$ = _SeqFile$'
    RUN_SEQUENCE_CMD = 'RunSequence "{data_dir}",, "{experiment_name}_{timestamp}"'


class RegisterFlag(Enum):
    def __str__(self):
        return '%s' % self.value

    # for table
    NUM_ROWS = "NumberOfRows"

    # for Method
    SOLVENT_A_COMPOSITION = "PumpChannel_CompositionPercentage"
    SOLVENT_B_COMPOSITION = "PumpChannel2_CompositionPercentage"
    SOLVENT_C_COMPOSITION = "PumpChannel3_CompositionPercentage"
    SOLVENT_D_COMPOSITION = "PumpChannel4_CompositionPercentage"
    FLOW = "Flow"
    MAX_TIME = "StopTime_Time"
    COLUMN_OVEN_TEMP1 = "TemperatureControl_Temperature"
    COLUMN_OVEN_TEMP2 = "TemperatureControl2_Temperature"
    STOPTIME_MODE = "StopTime_Mode"
    POSTIME_MODE = "PostTime_Mode"

    # for Method Timetable
    SOLVENT_COMPOSITION = "SolventComposition"

    # for Sequence
    VIAL_LOCATION = "Vial"
    NAME = ""
    METHOD = ""
    INJ_VOL = ""


class TableOperation(Enum):
    def __str__(self):
        return '%s' % self.value

    DELETE_TABLE = 'DelTab {register}, "{table_name}"'
    CREATE_TABLE = 'NewTab {register}, "{table_name}"'
    NEW_ROW = 'InsTabRow {register}, "{table_name}"'
    EDIT_ROW_VAL = 'SetTabVal "{register}", "{table_name}", {row}, "{col_name}", {val}'
    EDIT_ROW_TEXT = 'SetTabText "{register}", "{table_name}", {row}, "{col_name}", "{val}"'
    GET_ROW_VAL = 'TabVal ("{register}", "{table_name}", {row}, "{col_name}")'
    GET_ROW_TEXT = 'TabText ("{register}", "{table_name}", {row}, "{col_name}")'
    GET_OBJ_HDR_VAL = '{internal_val} = TabHdrVal({register}, "{table_name}", "{col_name}")'
    GET_OBJ_HDR_TEXT = ''
    UPDATE_OBJ_HDR_VAL = 'SetObjHdrVal {register}, {register_flag}, {val}'
    UPDATE_OBJ_HDR_TEXT = 'SetObjHdrText {register}, {register_flag}, {val}'
    NEW_COL_TEXT = 'NewColText {register}, "{table_name}", "{col_name}", "{val}"'
    NEW_COL_VAL = 'NewColVal {register}, "{table_name}", "{col_name}", {val}'


class PType(Enum):
    STR = "str"
    NUM = "num"


@dataclass
class Param:
    ptype: PType
    val: Union[float, int, str, Any]
    chemstation_key: Union[RegisterFlag, list[RegisterFlag]]


@dataclass
class HPLCMethodParams:
    organic_modifier: Param
    flow: Param
    temperature: Param
    inj_vol: Param
    equ_time: Param
    maximum_run_time: Param


@dataclass
class Entry:
    start_time: float
    organic_modifer: float
    flow: float


@dataclass
class SequenceEntry:
    vial_location: Optional[int] = None
    method: Optional[str] = None
    inj_vol: Optional[int] = None
    name: Optional[str] = None


@dataclass
class SequenceTable:
    rows: list[SequenceEntry]


@dataclass
class MethodTimetable:
    first_row: HPLCMethodParams
    subsequent_rows: list[Entry]
    dad_wavelengthes: Optional[list[Signal]] = None
    organic_modifier: Optional[SolventElement] = None
    modifier_a: Optional[SolventElement] = None


class HPLCRunningStatus(Enum):
    @classmethod
    def has_member_key(cls, key):
        return key in cls.__members__

    INJECTING = "INJECTING"
    PREPARING = "PREPARING"
    RUN = "RUN"
    NOTREADY = "NOTREADY"
    POSTRUN = "POSTRUN"
    RAWDATA = "RAWDATA"
    INITIALIZING = "INITIALIZING"
    NOMODULE = "NOMODULE"


class HPLCAvailStatus(Enum):
    @classmethod
    def has_member_key(cls, key):
        return key in cls.__members__

    PRERUN = "PRERUN"
    OFFLINE = "OFFLINE"
    STANDBY = "STANDBY"


class HPLCErrorStatus(Enum):

    @classmethod
    def has_member_key(cls, key):
        return key in cls.__members__

    ERROR = "ERROR"
    BREAK = "BREAK"
    NORESPONSE = "NORESPONSE"
    MALFORMED = "MALFORMED"


@dataclass
class Table:
    register: str
    name: str


def str_to_status(status: str) -> Union[HPLCAvailStatus, HPLCErrorStatus, HPLCRunningStatus]:
    if HPLCErrorStatus.has_member_key(status):
        return HPLCErrorStatus[status]
    if HPLCRunningStatus.has_member_key(status):
        return HPLCRunningStatus[status]
    if HPLCAvailStatus.has_member_key(status):
        return HPLCAvailStatus[status]
    raise KeyError(status)
