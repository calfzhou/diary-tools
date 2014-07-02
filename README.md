diary-tools
===========

Add Existing Diary to Git
-------------------------

Usage:

```
python -m diary.gitting_memory
```

Unpack:

```shell
for f in *.rar; do unrar x -p{xxxxx}`basename -s .rar $f` $f .; done
for d in 20??; do for f in $d/*.rar; do unrar x -p{xxxxx}`basename -s .rar $f` $f $d/; done; done
```

Workflow, Month branching:

```
for decade in (200x, 201x):
    mkdir decade && cd decade
    git init
    gitcrypt init
    create master branch

    foreach year in asc order:
        # git checkout master
        # git checkout -b year
        foreach month in asc order:
            git checkout master
                git checkout -b year-month
                mkdir {year}/{month}
                foreach day sort by mdate:
                    convert day.dia to utf-8 unix format
                    save the output as year/month/day.dia
                    git add && commit --date mdate
                # git checkout year
                # git merge --no-commit year-month
                # git commit --date max(whole month dia mdates)
```

Finalize One Year
-----------------

Usage:

```
python -m diary.finalize_year
```

Workflow:

```
git checkout {year}-01
for month in 02...12:
    git checkout {year}-{month}
    git rebase {year}-{month-1}

git checkout -b {year}
for month in 01...12:
    git branch -D {year}-{month}

if push:
    git push origin --delete {year}-{month}
    git push
```
