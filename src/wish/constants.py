import os
"""
Configuration parameters, app constants, os-specific tuning, etc. goes here.
This is basically a dumpster for globals.
"""

# MYREPOS = '/home/zeebrow/repos/github.com/zeebrow'
myrepos =  os.getenv('MYREPOS') if os.getenv('MYREPOS') != "" else None
if not myrepos:
    print("Uuuhhhh... ")
    os.exit(1)

repopath = myrepos + '/santapls/'
skelpath = repopath + 'prj-skel/'
archpath = repopath + 'archive/'
wishlist = repopath + 'wishlist.md'

skel = lambda wishname: f"""\
## {wishname}
________
### Synopsis

### Usage

```
{wishname}
```

### Would Require

### Difficulty


"""
