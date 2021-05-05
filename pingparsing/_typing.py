from datetime import datetime
from typing import Dict, Sequence, Union

import humanreadable as hr


TimeArg = Union[hr.Time, int, str, None]
IcmpReplies = Sequence[Dict[str, Union[str, bool, float, int, datetime]]]
PingAddOpts = Union[str, Sequence[str]]
