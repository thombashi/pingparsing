from datetime import datetime
from typing import Dict, Sequence, Union

import humanreadable as hr


TimeArg = Union[hr.Time, int, str, None]
IcmpReplies = Sequence[Dict[str, Union[bool, float, int, datetime]]]
