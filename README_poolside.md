# how to sync with upstream

```
git remote add upstream git@github.com:smacker/go-tree-sitter.git
git fetch upstream
git merge upstream/master # or some other branch that you want to merge with
```

There will be lots of conflicts. Unless we have changes we specifically made for poolside's use case and have not pushed to upstream, you probably will want to prefer upstream's version in any conflict.

Then you need to fix up some C header #include directives, mostly because upstream is OK with having Unix shortcuts in them but Forge cannot build with such. There is a python script in this repo to help you with that:

```
# in the root of go-tree-sitter repo:
./header_fix.py
```

If the script fails on some files, debug and fix the script and go again. Thank you very much. Make sure your merge commit and your script change commits are sepearate commits (OK to be in the same PR) so that it's easier to review the script changes.

*TODO: The script can generate new files. We do not have a good procedure to automatically clean them up during a merge with upstream.*