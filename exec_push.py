from subprocess import run
from json import load
from datetime import now

with open('./settings.json','r') as f:
    settings = load(f)

def push_commit_with_date(repo_dir, sha, remote, branch, when, tz_offset=None):
    """
    Push the commit `sha` to `remote`/`branch`, redated so it appears on
    GitHub's activity graph on `when`.

    Builds a new commit object (same tree + message as `sha`, parented on
    the branch's current remote tip if it exists) with author/committer
    date set to `when`, then pushes that. The original commit `sha` in
    your local repo is untouched.

    Args:
        repo_dir: path to the local git repo
        sha: commit-ish to base the push on (e.g. "HEAD", "abc1234")
        remote: remote name, e.g. "origin"
        branch: remote branch name to push to
        when: datetime object for the desired commit date
        tz_offset: e.g. "+0200"; defaults to the machine's current local offset

    Returns:
        the SHA of the new, redated commit that was pushed
    """
    def git(args, extra_env=None):
        import os
        env = os.environ.copy()
        if extra_env:
            env.update(extra_env)
        result = run(["git"] + args, cwd=repo_dir, capture_output=True, text=True, env=env)
        if result.returncode != 0:
            raise RuntimeError(f"git {' '.join(args)} failed:\n{result.stderr.strip()}")
        return result.stdout.strip()

    resolved_sha = git(["rev-parse", sha])
    tree = git(["rev-parse", f"{resolved_sha}^{{tree}}"])
    message = git(["log", "-1", "--format=%B", resolved_sha])

    if tz_offset is None:
        tz_offset = now().astimezone().strftime("%z")
    git_date = when.strftime("%Y-%m-%d %H:%M:%S") + " " + tz_offset

    parent_out = git(["ls-remote", "--heads", remote, branch])
    parent = parent_out.split()[0] if parent_out else None

    commit_tree_args = ["commit-tree", tree]
    if parent:
        commit_tree_args += ["-p", parent]
    commit_tree_args += ["-m", message]

    new_sha = git(
        commit_tree_args,
        extra_env={"GIT_AUTHOR_DATE": git_date, "GIT_COMMITTER_DATE": git_date},
    )

    git(["push", remote, f"{new_sha}:refs/heads/{branch}"])

    return new_sha

if __name__ == "__main__":

    push_commit_with_date("C:\\Users\\Main\\Desktop\\PROJEKTY\\GitDraw")