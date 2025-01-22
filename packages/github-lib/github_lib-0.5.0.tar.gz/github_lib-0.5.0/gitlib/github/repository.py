from typing import List
from github.Repository import Repository
from github import GithubException, RateLimitExceededException

from gitlib.common.exceptions import GitLibException
from gitlib.models.diff import Diff
from gitlib.github.commit import GitCommit


class GitRepo:
    """
        Represents a GitHub repository.
    """

    def __init__(self, repo: Repository):
        self.repo = repo

    @property
    def id(self):
        return self.repo.id

    @property
    def owner(self):
        return self.repo.owner

    @property
    def commits_count(self) -> int:
        return self.repo.get_commits().totalCount

    @property
    def language(self) -> str:
        return self.repo.language

    @property
    def description(self) -> str:
        return self.repo.description

    @property
    def size(self) -> int:
        return self.repo.size

    @property
    def stars(self) -> int:
        return self.repo.stargazers_count

    @property
    def forks(self) -> int:
        return self.repo.forks_count

    @property
    def watchers(self) -> int:
        return self.repo.watchers_count

    @property
    def name(self) -> str:
        return self.repo.name

    def get_commit(self, sha: str, raise_err: bool = False) -> GitCommit | None:
        # Ignore unavailable commits
        try:
            # self.app.log.info(f"Getting commit {commit_sha}")
            return GitCommit(self.repo.get_commit(sha=sha))
        except (ValueError, GithubException):
            err_msg = f"Commit {sha} for repo {self.repo.name} unavailable."
        except RateLimitExceededException as rle:
            err_msg = f"Rate limit exhausted: {rle}"

        if raise_err:
            raise GitLibException(err_msg)

        # TODO: implement some logging

        return None

    def get_diff(self) -> Diff:
        # TODO: use the repo.compare(base, head) to get the diff between the commit and its parent
        pass

    def get_versions(self, limit: int = None) -> List[str]:
        releases = self.repo.get_releases()

        if releases.totalCount > 0:
            if limit and releases.totalCount > limit:
                # Return the latest n releases
                return [release.tag_name for release in releases[:limit]]
            else:
                return [release.tag_name for release in releases]
        else:
            tags = self.repo.get_tags()

            if limit and tags.totalCount > limit:
                return [tag.name for tag in tags[:limit]]
            else:
                return [tag.name for tag in tags]
