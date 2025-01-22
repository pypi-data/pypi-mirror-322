from pygit2 import Diff
from gitlib import GitClient

TOKEN = "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"

client = GitClient(token=TOKEN)
repo = client.get_repo(owner="ArtifexSoftware", project="mujs")
print(repo)

commit = repo.get_commit(sha="fa3d30fd18c348bb4b1f3858fb860f4fcd4b2045")
print(commit)

diff = commit.get_diff(unified=True)

print(diff)

# Compare with pygit2 diff
parsed_diff = Diff.parse_diff(commit.diff)

for patch in parsed_diff:
    print(patch.delta.old_file.path, patch.delta.new_file.path)
    print(patch.delta.similarity)

    for hunk in patch.hunks:
        print("\t", hunk.old_start, hunk.new_start, hunk.header)
        for line in hunk.lines:
            print("\t\t", line.origin, line.old_lineno, line.new_lineno)
