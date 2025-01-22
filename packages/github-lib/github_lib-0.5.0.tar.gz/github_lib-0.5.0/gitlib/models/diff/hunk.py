from typing import List
from pydantic import BaseModel

from gitlib.models.diff.line import DiffLine


class DiffHunk(BaseModel):
    order: int
    old_lines: List[DiffLine]
    new_lines: List[DiffLine]
    old_start: int
    new_start: int

    @property
    def ordered_lines(self) -> List[DiffLine]:
        """
        Returns all lines (old and new) in a single list sorted by line number.

        Returns:
            List[DiffLine]: A list of all lines sorted by their line numbers.
        """
        return sorted(self.old_lines + self.new_lines, key=lambda x: x.lineno)

    @property
    def deletions(self):
        return len(self.old_lines)

    @property
    def insertions(self):
        return len(self.new_lines)

    def __str__(self):
        header = f"{self.order} {self.__class__.__name__}({self.old_start}, {self.new_start})"

        for line in self.ordered_lines:
            if line.skip:
                continue
            # TODO: should account for padding size given the line number
            if line.type.value == '-':
                header += f"\n\t{line.lineno}     {line.type.value} {line.content}"
            else:
                header += f"\n\t    {line.lineno} {line.type.value} {line.content}"

        return header
