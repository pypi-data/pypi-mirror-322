from gitlib.models.url.base import GithubUrl


class GithubRepoUrl(GithubUrl):
    owner: str
    repo: str
