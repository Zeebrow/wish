from os.path import sep
from shutil import rmtree
import logging
import click
from git import Repo
import constants as C
from ls import _get_wishes
logger = logging.getLogger(__name__)

@click.command()
@click.argument('wish')
def delete(wish):
    """
    Removes a wish from wishlist.md, and completely removes its project skeleton.
    """
    # inverse of ls.get_wish()
    if wish not in _get_wishes():
        logger.warning(f"Wish not found: {wish}")
        return None

    with open(C.wishlist, 'r') as wl:
        lines = wl.readlines()
        logger.debug(f"Read {len(lines)} lines")
    with open(C.wishlist, 'w') as wl:
        _linect = 0
        keep_output = True
        for line in lines:
            if line.startswith('## ') and not keep_output:
                keep_output = True
            if line.startswith(f'## {wish}'):
                keep_output = False
            if keep_output:
                wl.write(line)
            else:
                _linect += 1
        logger.debug(f"Removed {_linect} lines from {C.wishlist}.")

    repo = Repo(C.repopath)
    repo.index.add(C.wishlist)
    commit_message = ""
    _commit = repo.index.commit(message=commit_message)
    logger.debug(f"wishlist commit results: {_commit}")
    remote = repo.remote()
    push_results = remote.push()
    logger.debug(f"wishlist push results: {push_results}")
    del_skel(wish)

def del_skel(wish, commit_message=None):
    if not commit_message:
        commit_message=f"Adding wish: {wish}"
    deldir = C.skelpath + wish
    try:
        rmtree(deldir)
        logger.debug(f"Removed directory: {deldir}")
    except FileNotFoundError as e:
        logger.warning(e)

    repo = Repo(C.repopath)
    try:
        _git_debug = repo.index.remove(deldir, r=True)
    except Exception as e:
        logger.critical(f"Could not remove direcotry tree '{deldir}' for wish '{wish}': {e}")
        exit(1)
    logger.debug(f"Git remove directory ({deldir}) results: {_git_debug}")
    _commit = repo.index.commit(message=f"Removed '{deldir}' project skelington for '{wish}'.")
    logger.debug(f"Removed '{deldir}' project skelington for '{wish}'.")
    remote = repo.remote()
    push_results = remote.push()
    logger.debug(f"Remove {deldir} push results: {push_results}")
