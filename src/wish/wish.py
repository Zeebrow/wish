import logging
from os import stat, path
import pathlib
from textwrap import dedent
from shutil import rmtree
from git import Repo
import re

import constants as C
logger = logging.getLogger(__name__)



class Wish:
    """
    Wishes are the 'main' uint of data
    Wish manages the contents to be committed to git by Wishlist
    """
    def __init__(self, wish):
        self.name = wish
        self.prj_path = C.prj_skel_path(self.name)
        self.readme = C.wish_readme(self.name)
        self.block = self._load_text()
        self.exists = False if self.block == '' else True

    def __repr__(self):
        return self.name

    def _load_text(self) -> str:
        # hear ye, hear ye
        # wishlist.md is the source of truth
        # not prj_skel README
        r = re.compile("^##\s+(.*)$")
        mdtext = ''
        with open(C.wishlist, 'r') as wl:
            _print_output = False
            _ct = 0
            for line in wl:
                m = r.match(line)
                if m and _print_output:
                    print(f"found {m.groups()[0]}")
                    _print_output = False
                if _print_output:
                    _ct += 1
                    mdtext += line
                if (m) and (m.groups()[0] == self.name):
                    _ct += 1
                    _print_output = True
                    mdtext += line
        logger.debug(f"Got {_ct} lines for wish '{self.name}'.")
        return mdtext

    def del_wish(self) -> bool:
        # update wishlist
        if not self.exists:
            logger.error(f"Can't delete wish '{self}' - does not exist!")
            return False
        with open(C.wishlist, 'r') as wl:
            lines = wl.readlines()
        with open(C.wishlist, 'w') as wl:
            keep_output = True
            for line in lines:
                if line.startswith("## ") and not keep_output:
                    keep_output = True
                if line.startswith(f"## {self.name}"):
                    keep_output = False
                if keep_output:
                    wl.write(line)
        rmtree(self.prj_path)

        # cleanliness
        self.block = None
        self.skel = None
        self.name = "." + self.name
        return True

    def _print(self) -> None:
        print(self.block)

    def _set_block(self, mdtext) -> bool:
        if self.block == '':
            self.block = C.new_wish_skel(self.name)
        else:
            self.block = mdtext
        return True

    def make_new(self, mdtext):
        self._set_block(mdtext)
        self._write_block_to_prj_skel()
        with open(C.wishlist, 'a') as wl:
            wl.write(self.block)

    def _write_block_to_prj_skel(self):
        self.prj_path.mkdir(parents=True, exist_ok=True)
        with open(self.readme, 'w') as sk:
            sk.write(self.block)
        
    def _edit_wish(self):
        if self.block == '':
            logger.warning(f"Cannot edit wish '{self.name}' - does not exist!")
            return
        with open(C.wishlist, 'r') as wl:
            before_wish = ''
            after_wish = ''
            append_output=False
            b4 = True
            after = False

            for line in wl:
                if line.startswith(f'## ') and append_output:
                    after = True
                    append_output = False
                if append_output:
                    print("--" + line.strip())
                if line.startswith(f'## {self.name}'):
                    b4 = False
                    append_output = True
                if b4:
                    before_wish += line
                if after:
                    after_wish += line
        with open(C.wishlist, 'w') as nw:
            nw.write(before_wish)
            nw.write(self.block)
            nw.write(after_wish)

    def _delete(self):
        pass

