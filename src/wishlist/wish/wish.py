import logging
import re
from os import stat, path
import pathlib
from textwrap import dedent
from shutil import rmtree
import tempfile
from pathlib import Path
from git import Repo

from . import constants as C
from . import prettyprint_mdtext

logger = logging.getLogger(__name__)

class Wish:
    """
    Wishes are the 'main' uint of data
    Wish manages the contents to be committed to git by Wishlist
    """
    def __init__(self, wishname, repo_path=C.repo_path):
        self._r = C.wish_regex
        self.name = wishname
        self.repo_path = Path(repo_path)
        self.wishlist_file = self.repo_path / "wishlist.md"
        self.prj_path = self.repo_path / "prj-skel"
        #self.prj_path = C.prj_skel_path(self.name)
        self.readme = self.prj_path / "README.md"
        #self.readme = C.wish_readme(self.name)
        self.before = None
        self.after = None
        self.block = None
        self._load_wish()
        self.exists = False if self.block is None else True

    def __repr__(self):
        return self.name

    def _load_wish(self):
        with open(self.wishlist_file, 'r') as wl:
            self.before = ''
            self.after = ''

            append_output=False
            b4 = True
            after = False

            for line in wl:
                m = self._r.match(line)
                if m and append_output:
                    after = True
                    append_output = False
                if append_output:
                    self.block += line
                    #print("--" + line.strip())
                if m and m.groups()[0] == self.name:
                    self.block = line
                    b4 = False
                    append_output = True
                if b4:
                    self.before += line
                if after:
                    self.after += line

    def create(self):
        # whats the difference between below and 'if not self.block'?
        if self.block is not None:
            logger.error(f"Cannot create new wish '{self.name}' - already exists!")
            return
        self.block = C.new_wish_skel(self.name)
        self._write_wishlist()
        self._write_block_to_prj_skel()
        self._commit()
        logger.debug(f"Created new wish '{self.name}'.")

    def pprint(self, raw=False, mdtext='', filename=''):
        if raw:
            print(self.block)
            return
        if mdtext == '':
            prettyprint_mdtext.format_mdtext(mdtext=self.block)

    def update(self, mdtext):
        self.block = mdtext
        self._write_wishlist()
        self._write_block_to_prj_skel()
        self._commit()
        logger.debug(f"Updated wish '{self.name}'.")


    def delete(self):
        self.block = ''
        self._write_wishlist()
        self._remove_prj_skel()
        logger.debug(f"Deleted wish '{self.name}' and associated project.")

    def _write_wishlist(self):
        #tmp_wl = tempfile.mktemp(mode='w+b')
        b = 0
        with open(self.wishlist_file, 'w') as wl:
            b += wl.write(self.before)
            b += wl.write(self.block)
            b += wl.write(self.after)
        logger.debug(f"Wrote {b} bytes to '{self.wishlist_file}'.")

    def _remove_prj_skel(self):
        rmtree(self.prj_path)
        logger.debug(f"Removed project {self.prj_path} for wish '{self.name}'")

    def _write_block_to_prj_skel(self):
        self.prj_path.mkdir(parents=True, exist_ok=True)
        with open(self.readme, 'w') as sk:
            b = sk.write(self.block)
        logger.debug(f"Wrote {b} bytes to '{self.readme}' for wish '{self.name}'.")

    def _commit(self, msg='', push=False):
        """
        Commit changes to git and push
        """
        return
        if msg == '':
            msg = "Committing change..."
            logger.warning(f"Using generic commit message...")
        self.repo.index.add(str(C.wishlist))
        self.repo.index.add(str(C.wish_readme(wishname)))
        self.repo.index.commit(message=msg)
        if push:
            remote = self.repo.remote()
            remote.push()
