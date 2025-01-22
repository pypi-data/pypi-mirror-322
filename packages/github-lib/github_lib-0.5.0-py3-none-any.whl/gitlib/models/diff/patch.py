from pydantic import BaseModel
from typing import List, Iterator

from gitlib.models.diff.hunk import DiffHunk
from gitlib.models.diff.file import DiffFile


class Patch(BaseModel):
    hunks: List[DiffHunk]
    # old_file: DiffFile
    # new_file: DiffFile

    def __iter__(self) -> Iterator[DiffHunk]:
        return iter(self.patches)

    def __str__(self):
        return "\n".join(str(hunk) for hunk in self.hunks)
