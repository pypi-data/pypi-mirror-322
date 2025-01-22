import requests

from typing import List
from github.Commit import Commit

from gitlib.models.diff import Diff
from gitlib.github.file import GitFile
from gitlib.parsers.diff.git import GitDiffParser
from gitlib.parsers.diff.unified import UnifiedDiffParser


class GitCommit:
    def __init__(self, commit: Commit):
        self.commit = commit
        self._files = None
        self._diff = None

    @property
    def parents(self):
        return self.commit.parents

    @property
    def html_url(self):
        return self.commit.html_url

    @property
    def message(self):
        return self.commit.commit.message

    @property
    def sha(self):
        return self.commit.sha

    @property
    def date(self):
        return self.commit.commit.author.date

    @property
    def stats(self):
        return self.commit.stats

    @property
    def state(self):
        return self.commit.get_combined_status().state

    @property
    def files(self) -> List[GitFile]:
        if self._files is None:
            self._files = [GitFile(file) for file in self.commit.files]
        return self._files

    @property
    def diff(self) -> str:
        # Lazy load the diff
        if not self._diff:
            self._diff = requests.get(f"{self.commit.html_url}.diff").text

        return self._diff

    def get_diff(self, unified: bool = False) -> Diff:
        """
            By default, the diff is obtained by using the diff URL.

            :param unified: If True, uses UnifiedPatchParser over the self.commit.files to get the diff.
        """
        if unified:
            patches = []

            for file in self.files:
                # TODO: implement the case when the commit has more than one parent
                # if len(self.commit.parents) > 1:
                #    raise NotImplemented(f"Commit {self.commit.sha} has more than one parent.")

                # TODO: change this to work for the UnifiedPatchParser by passing the old_file
                patch = file.get_patch()
                patches.append(patch)

            parser = UnifiedDiffParser(patches)
        else:
            parser = GitDiffParser(self.diff)

        return parser()
