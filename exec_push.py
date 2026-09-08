from subprocess import run
from json import load, dump, loads, dumps
from datetime import datetime, date

with open('./settings.json','r') as f:
    settings = load(f)

def push_commit_with_date(repo_dir, sha, remote, branch, when = None, tz_offset=None):

    def git(args, extra_env=None):
        import os
        env = os.environ.copy()
        if extra_env:
            env.update(extra_env)
        result = run([settings["ORIGINAL_PATH"]] + args, cwd=repo_dir, capture_output=True, text=True, env=env)
        if result.returncode != 0:
            raise RuntimeError(f"git {' '.join(args)} failed:\n{result.stderr.strip()}")
        return result.stdout.strip()

    resolved_sha = git(["rev-parse", sha])

    if when == None:
        git(["push", remote, f"{resolved_sha}:refs/heads/{branch}"])
        return resolved_sha

    tree = git(["rev-parse", f"{resolved_sha}^{{tree}}"])
    message = git(["log", "-1", "--format=%B", resolved_sha])

    if tz_offset is None:
        tz_offset = datetime.now().astimezone().strftime("%z")
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

def main():

    with open('./que.txt','r',encoding='UTF-8') as f:

        que = [loads(l) for l in f.read().split('|\n')]

    with open('./times.txt','r',encoding='UTF-8') as f:

        times = load(f)

    if str(date.today()) in times:

        while times[str(date.today())] > 0:
            
            try:
                push = que.pop(0)
            except IndexError:
                break
            
            push_commit_with_date(
                repo_dir=push['repo_path'],
                sha=push['sha'],
                remote=push['remote'],
                branch=push['remote_branch'],
                when=datetime.now()
            )
            times[str(date.today())] -= 1

    with open('./que.txt','w',encoding='UTF-8') as f:
    
        f.write('|\n'.join([dumps(v) for v in que]))
    
    with open('./times.txt','r',encoding='UTF-8') as f:
    
        times = dump(times, f)


if __name__ == "__main__":

    main()