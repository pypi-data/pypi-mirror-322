from pydantic import BaseModel
from typing import List, Iterator

from gitlib.models.diff.hunk import DiffHunk


class Patch(BaseModel):
    hunks: List[DiffHunk]
    old_file: str
    new_file: str

    def __iter__(self) -> Iterator[DiffHunk]:
        return iter(self.patches)

    def __str__(self):
        return "\n".join(str(hunk) for hunk in self.hunks)
