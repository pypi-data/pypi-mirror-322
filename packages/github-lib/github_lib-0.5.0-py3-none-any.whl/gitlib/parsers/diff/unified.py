from typing import List

from gitlib.models.diff import Diff
from gitlib.models.diff.patch import Patch
from gitlib.parsers.diff.base import DiffParser


class UnifiedDiffParser(DiffParser):
    def __init__(self, patches: List[Patch], **kwargs):
        super().__init__(**kwargs)
        self.patches = patches

    def __call__(self) -> Diff:
        return Diff(patches=self.patches)
