from typing import List, Iterator
from pydantic import BaseModel


from gitlib.models.diff.patch import Patch


class Diff(BaseModel):
    patches: List[Patch]

    def __iter__(self) -> Iterator[Patch]:
        return iter(self.patches)

    def __str__(self):
        return "\n".join(str(_patch) for _patch in self.patches)
