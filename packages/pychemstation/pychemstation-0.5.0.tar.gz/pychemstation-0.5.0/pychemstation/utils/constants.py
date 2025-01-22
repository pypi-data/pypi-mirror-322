from ..utils.table_types import Table

# maximum command number
MAX_CMD_NO = 255

# tables
METHOD_TIMETABLE = Table(
    register="RCPMP1Method[1]",
    name="Timetable"
)

SEQUENCE_TABLE = Table(
    register="_sequence[1]",
    name="SeqTable1"
)
