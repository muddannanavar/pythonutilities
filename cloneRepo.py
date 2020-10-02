#!/usr/bin/env python
import git
from pathlib import Path
import shutil

repo_url="https://github.com/muddannanavar/pythonutilities.git"
local_repo="testrx"

#cleanup if repos exists
try:
    dirpath = Path('./', local_repo)
    #if dirpath.exists() and local_repo.is_dir():
    if dirpath.is_dir():
        print(f"Deleting dir {dirpath}")
        shutil.rmtree(local_repo)    
except Exception as e:
    print(f"Check if {local_repo} if valid or exists")
    exit(3)

try:
    repo = git.Repo.clone_from(repo_url, local_repo)
except Exception as e:
    print(f"Please check {repo_url} or access to it")
    exit (1)
