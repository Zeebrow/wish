import tempfile
from getpass import getuser
from textwrap import dedent
import logging
import os
from os.path import sep

import click
from git import Repo
from git.objects.commit import Commit

import constants as C
logger = logging.getLogger(__name__)


@click.command()
@click.argument('wish')
@click.option('--no-commit')
def new_wish(wish, debug=False, no_commit=True):
    """
    Create a new wish.

    Appends the wish to wishlist.md, and creates a project skeleton with a README.md (for some reason)
    """
    text = _stage_new_wish(wish=wish,debug=debug, no_commit=no_commit)
    if not text:
        logger.debug("no-commit flag specified, exiting.")
    commit_wish(wish=wish, text=text)
    create_skel(wish=wish, text=text)

def _stage_new_wish(wish, debug, no_commit):
    block = \
    f"""    ## {wish}
    ________
    ### Synopsis

    ### Usage

    ```
    {wish}
    ```

    ### Would Require

    ### Difficulty


    """
    block = dedent(block)
    block = click.edit(block, require_save=True, extension='.md')
    if not block:
        logger.warning(f"Wish '{wish}' not created - changes were not saved.")
        return None
    if debug:
        fname = tempfile.mkstemp(text=True, prefix=f"{wish}-", suffix=".tmp")
        print(f"fname: {fname}")
        with open(fname[1], 'w') as f:
            f.write(dedent(block))
    return block

def commit_wish(wish, text, commit_message=None):
    if not commit_message:
        commit_message=f"Adding wish: {wish}"
    with open(C.wishlist, 'a') as wl:
        wl.write(text)

    logger.debug(f"Appended wish '{wish}' to {C.wishlist}")
    print("committing...")
    repo = Repo(C.repopath)
    repo.index.add(C.wishlist)
    _commit = repo.index.commit(message=commit_message)
    logger.debug(f"wishlist commit results: {_commit}")
    remote = repo.remote()
    push_results = remote.push()
    logger.debug(f"wishlist push results: {push_results}")


def create_skel(wish, text: str):
    # newdir = C.repopath + os.pathsep + wish
    logger.debug(f"executing create_sket({wish}, 'text')")
    newdir = C.skelpath + wish
    logger.debug(f"Created new directory: {newdir}")
    os.mkdir(newdir)
    os.stat(newdir)
    repo = Repo(C.repopath)
    # new_readme = newdir + os.pathsep + 'README.md'
    new_readme = newdir + sep + 'README.md'
    readme_text = text.replace('## ', '# ')
    with open(new_readme, 'w') as f:
        f.write(readme_text)
    logger.debug(f"Created README.md for wish '{wish}' at {new_readme}")
    _git_debug = repo.index.add(new_readme)
    logger.debug(f"Add file (index) results: {_git_debug}")
    _commit = repo.index.commit(message=f"Create readme for new wish project '{wish}'.")
    logger.debug(f"new readme commit results: {_commit}")
    remote = repo.remote()
    push_results = remote.push()
    logger.debug(f"new readme push results: {push_results}")

