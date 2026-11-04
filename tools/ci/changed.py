"""Only explanatory docs may bypass application verification; unknown paths build."""
import os
import subprocess

DOCS_ONLY = frozenset({"README.md", "docs/SEMANTIC_MATTER.md"})


def needs_application(paths, event):
    return event != "pull_request" or not set(paths).issubset(DOCS_ONLY)


if __name__ == "__main__":
    event = os.environ["GITHUB_EVENT_NAME"]
    # pull_request checkout is GitHub's tested merge commit; its first parent
    # is the base. --no-renames exposes both sides of a rename/deletion.
    paths = subprocess.check_output(
        ["git", "diff", "--no-renames", "--name-only", "-z", "HEAD^1", "HEAD"]
    ).decode().split("\0")[:-1] if event == "pull_request" else []
    print("application=" + str(needs_application(paths, event)).lower())
