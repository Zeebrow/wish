from os import getenv
from os.path import sep
from pathlib import Path
import re

"""
Configuration parameters, app constants, os-specific tuning, etc. goes here.
This is basically a dumpster for globals.
"""
# MYREPOS = '/home/zeebrow/repos/github.com/zeebrow'
wishlist_home =  getenv('WISHLIST_HOME') if getenv('WISHLIST_HOME') != "" else None
if not wishlist_home:
    # TODO: XDG_DATA_DIR
    # getenv('')
    print("Uuuhhhh... ")
    exit(1)

fmt_md_binary = Path(wishlist_home + "/wish/src/plugins/fmt_md_text")
#print(os.stat(fmt_md_binary))

# repo_path = wishlist_home + f'{sep}santapls{sep}'
# prj_skel_path = repo_path + f'prj-skel{sep}'
# archive_path = repo_path + f'archive{sep}'
# wishlist = repo_path + 'wishlist.md'
repo_path = Path(wishlist_home) 
archive_path = repo_path / 'archive'
wishlist = repo_path / 'wishlist.md'
prj_skel_path = lambda wishname: repo_path / 'prj-skel' / wishname
wish_readme = lambda wishname: prj_skel_path(wishname) / 'README.md'
new_wish_skel = lambda wishname: f"""\
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

wish_regex = re.compile("^##\s+(.*)$")

if __name__ == '__main__':
    print(repo_path)
    print(prj_skel_path('some_weesh'))
    print(archive_path)
    print(wishlist)
    print(wish_readme('some_wish'))
