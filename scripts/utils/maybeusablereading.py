from math import isinf, isnan
from typing import Optional

from .maybe import Maybe

class MaybeUsableReading(Maybe):
    def __init__(self, value:Optional[float]) -> None:
        if value is None:
            super().__init__(None)
            return

        if isinf(value) or isnan(value):
            super().__init__(None)
            return

        super().__init__(value)
