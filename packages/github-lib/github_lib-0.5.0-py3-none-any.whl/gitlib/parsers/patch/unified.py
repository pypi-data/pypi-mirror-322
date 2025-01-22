import difflib

from gitlib.parsers.patch.base import PatchParser, DiffHunkParser


class UnifiedPatchParser(PatchParser):
    """ Parser to process the changes and their location in code from patches

        Attributes:
            :param a_str: The contents of file A.
            :param b_str: The contents of file B.
    """
    def __init__(self, a_str: str, b_str: str, old_file: str, new_file: str, **kwargs):
        super().__init__(**kwargs)
        self.old_file = old_file
        self.new_file = new_file
        self.lines = list(difflib.unified_diff(a=a_str.splitlines(keepends=True), b=b_str.splitlines(keepends=True)))
        self.diff_hunk_parser = DiffHunkParser
