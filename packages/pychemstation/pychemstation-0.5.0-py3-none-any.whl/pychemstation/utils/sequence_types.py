from dataclasses import dataclass
from enum import Enum
from typing import Optional


@dataclass
class TrayLocation:
    row: str
    col: int


@dataclass
class SequenceDataFiles:
    sequence_name: str
    dir: str
    child_dirs: list[str]


class SampleType(Enum):
    SAMPLE = 1
    BLANK = 2
    CALIBRATION = 3
    CONTROL = 4


class InjectionSource(Enum):
    AS_METHOD = "As Method"
    MANUAL = "Manual"
    MSD = "MSD"
    HIP_ALS = "HipAls"


@dataclass
class SequenceEntry:
    sample_name: str
    vial_location: int
    method: Optional[str] = None
    num_inj: Optional[int] = 1
    inj_vol: Optional[int] = 2
    inj_source: Optional[InjectionSource] = InjectionSource.HIP_ALS
    sample_type: Optional[SampleType] = SampleType.SAMPLE


@dataclass
class SequenceTable:
    name: str
    rows: list[SequenceEntry]
