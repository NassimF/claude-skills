#!/usr/bin/env python3
"""Walk current directory (max depth 3) and print paths of git repos."""
import os
import sys

root = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
max_depth = 3

for dirpath, dirnames, filenames in os.walk(root):
    depth = dirpath[len(root):].count(os.sep)
    if depth >= max_depth:
        dirnames.clear()
        continue
    if '.git' in dirnames:
        print(os.path.abspath(dirpath))
        dirnames.clear()  # don't recurse into a repo
