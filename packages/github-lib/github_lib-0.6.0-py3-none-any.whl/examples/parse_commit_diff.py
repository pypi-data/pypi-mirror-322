from gitlib import GitClient

TOKEN = "YOUR_GITHUB_TOKEN_HERE"

client = GitClient(token=TOKEN)
repo = client.get_repo(owner="ArtifexSoftware", project="mujs")
print(repo)

commit = repo.get_commit(sha="fa3d30fd18c348bb4b1f3858fb860f4fcd4b2045")
print(commit)

commit_diff = commit.get_diff()

print("# COMMIT DIFF #")
print(commit_diff)


print("# REPO UNIFIED DIFF #")
repo_diff = repo.get_diff(commit.parents[0].sha, commit.sha)
print(repo_diff)
