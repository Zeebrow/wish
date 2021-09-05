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
        self._r = C.wish_regex
        #self._r = re.compile("^##\s+(.*)$")
        self.name = wish
        self.prj_path = C.prj_skel_path(self.name)
        self.readme = C.wish_readme(self.name)
        self.before = None
        self.after = None
        self.block = None
        self._load_wish()
        self.exists = False if self.block is None else True

    def __repr__(self):
        return self.name

    def _load_wish(self):
        with open(C.wishlist, 'r') as wl:
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
#        with open(C.wishlist, 'w') as nw:
#            nw.write(before_wish)
#            nw.write(self.block)
#            nw.write(after_wish)

#    def del_wish(self) -> bool:
#        # update wishlist
#        if not self.exists:
#            logger.error(f"Can't delete wish '{self}' - does not exist!")
#            return False
#        with open(C.wishlist, 'r') as wl:
#            lines = wl.readlines()
#        with open(C.wishlist, 'w') as wl:
#            keep_output = True
#            for line in lines:
#                m = self._r.match(line)
#                if m and not keep_output:
#                #if line.startswith("## ") and not keep_output:
#                    keep_output = True
#                if line.startswith(f"## {self.name}"):
#                    keep_output = False
#                if keep_output:
#                    wl.write(line)
#        rmtree(self.prj_path)
#
#        # cleanliness
#        self.block = None
#        self.skel = None
#        self.name = "." + self.name
#        return True


    def show(self) -> None:
        print(self.block)

#    def _set_block(self, mdtext) -> bool:
#        if self.block == '':
#            self.block = C.new_wish_skel(self.name)
#        else:
#            self.block = mdtext
#        return True

    def create(self):
        # whats the difference between below and 'if not self.block'?
        if self.block is not None:
            logger.error(f"Cannot create new wish '{self.name}' - already exists!")
            return
        self.block = C.new_wish_skel(self.name)
        #self._write_block_to_prj_skel()
        #with open(C.wishlist, 'a') as wl:
        #    wl.write(self.block)
    def update(self, mdtext):
        self.block = mdtext

    def write_block_to_prj_skel(self):
        self.prj_path.mkdir(parents=True, exist_ok=True)
        with open(self.readme, 'w') as sk:
            sk.write(self.block)

    def _delete(self):
        self.block = ''

