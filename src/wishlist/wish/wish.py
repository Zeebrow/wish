import logging
from os import stat, path
import os
import shutil
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
        self.prj_path = self.repo_path / "prj-skel" / self.name
        self.readme = self.prj_path / "README.md"
        self.before = ''
        self.block = ''
        self.after = ''
        # careful with _load_wish(). This may cause a bug in the future, if
        # initializing multiple new wishes before calling create() on any 
        # one of them.
        self._load_wish()
        self.exists = self._check_exists()

    def __repr__(self):
        return self.name

    def _load_wish(self):
        with open(self.wishlist_file, 'r') as wl:
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
        if self.block != '':
            logger.error(f"Cannot create new wish '{self.name}' - already exists!")
            raise ValueError(f"Cannot create new wish '{self.name}' - already exists!")
        self.block = C.new_wish_skel(self.name)

        self._write_wishlist()
        self._write_block_to_prj_skel()
        self._commit()
        logger.debug(f"Created new wish '{self.name}'.")
        return self._check_exists()

    def pprint(self, raw=False, mdtext=''):
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


    def delete(self) -> bool:
        if self.block == '':
            logger.warning(f"Could not delete wish '{self}': Does not exist.")
            raise ValueError(f"Could not delete wish '{self}': Does not exist.")
        self.block = ''
        self._write_wishlist()
        self._remove_prj_skel()
        logger.debug(f"Deleted wish '{self.name}'.")
        return not self._check_exists()

    def _check_exists(self) -> bool:
        """Re-loads self.before, self.after, and self.block from wishlist."""
        self.before = ''
        self.block = ''
        self.after = ''
        self._load_wish()
        self.exists = False if self.block == '' else True
        return self.exists

    def _write_wishlist(self):
        tmp_wl = tempfile.mktemp()
        b = 0
        with open(tmp_wl, 'w') as wl:
            b += wl.write(self.before)
            b += wl.write(self.block)
            b += wl.write(self.after)
        try:
            os.remove(self.wishlist_file)
            shutil.copyfile(tmp_wl, self.wishlist_file)
            logger.debug(f"Wrote {b} bytes to '{self.wishlist_file}'.")
        except Exception as e:
            logger.critical(f"Could not replace existing wishlist file '{self.wishlist_file}': {e}")
        finally:
            os.remove(tmp_wl)

    def _remove_prj_skel(self):
        try:
            rmtree(self.prj_path)
            logger.debug(f"Removed project {self.prj_path} for wish '{self.name}'")
            return
        except FileNotFoundError as e:
            logger.warning(f"Wish '{self.name}' has no associated project to delete!")
            return

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
        self.repo.index.add(str(self.wishlist_file))
        self.repo.index.add(str(self.readme))
        self.repo.index.commit(message=msg)
        if push:
            remote = self.repo.remote()
            remote.push()
