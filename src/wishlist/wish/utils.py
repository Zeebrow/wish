import logging
import re

from git import Repo

from . import constants as C
from . import wish 
logger = logging.getLogger(__name__)

def get_wishes(wishlist_file=C.wishlist):
    """
    click command 'ls'
    Returns list of wishes
    """
    _regex = C.wish_regex
    wishlist = []
    with open(wishlist_file, 'r') as wl:
        for line in wl:
            m = _regex.match(line)
            if m:
                wishlist.append(m.groups()[0].strip())
    return wishlist

def check_prj_readme(w: wish.Wish) -> bool:

    try:
        with open(w.readme, 'r') as rm:
            lines = rm.read()
            if lines == w.block:
                return True
            else:
                return False
    except FileNotFoundError:
        return False

def commit(prj_path, repo=C.repo_path):
    repo = Repo(repo / prj_path)
    pass
