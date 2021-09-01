import logging
from textwrap import dedent
from os.path import sep
from shutil import rmtree
from git import Repo

import constants as C

logger = logging.getLogger(__name__)

class Wishlist:
    """
    Wishlist is a collection of Wish objects
    Responsible for managing git state
    """
    def __init__(self, repopath=C.repopath):
        self.wishlist = C.wishlist
        self.wishes = []
        self._set_wishes()
        self.repo = Repo(repopath)

    def get_wishes(self):
        """
        click command 'ls'
        Returns list of wishes
        """
        wl = []
        for w in self.wishes:
            wl.append(w.name)
        return wl

    def get_wish(self, wish):
        """
        Returns raw markdown text representation of `wish`
        or None if wish doesn't exist
        """
        if not self._wish_exists(wish):
            logger.warning(f"No such wish: {wish} - try wish make {wish} to create")
            #click.echo(f"No such wish: {wish} - try wish make {wish} to create")
            return None
        logger.debug(f"Getting block for '{wish}'")
        for w in self.wishes:
            if w.name == wish:
                return w.block


    def del_wish(self, wish, commit_message="", push=True):
        """
        Remove wish from list.
        Returns True on success or None otherwise.
        """
        if not self._wish_exists(wish):
            logger.warning(f"Cannot remove wish '{wish}': does not exist")
            return None
        w = Wish(wish)
        w.del_wish()
        # r=True is saying 'git rm -r'
        self.repo.index.remove(C.skelpath + wish, r=True)
        self.repo.index.add(C.wishlist)
        self._commit(msg=f"Delete wish '{wish}'")

        # not strictly necessary, as the program will exit shortly after del_wish() returns.
        self.wishes.remove(wish)
        return True

    def add_wish(self, wish, mdtext):
        w = Wish(wish)
        w.add(mdtext)

        # sanitary
        self.wishes.append(w)
        pass

    def _wish_exists(self, wish):      
        return True if wish in self.get_wishes() else False

    def _set_wishes(self) -> list:
        """
        Set wishes list
        """
        with open(C.wishlist, 'r') as wl:
            for line in wl:
                if line.startswith("## "):
                    w = ''.join(line.strip().split(' ')[1:])
                    # self.wishes.append(w)
                    self.wishes.append(Wish(w))
        #return _wishes

    def _commit(self, msg=''):
        """
        Commit changes to git and push
        """
        if msg == '':
            msg = "Committing change..."
            logger.warning(f"Using generic commit message...")
        self.repo.index.commit(message=msg)
        remote = self.repo.remote()
        #remote.push()
        self._set_wishes()

class Wish:
    """
    Wishes are the 'main' uint of data
    Wish manages the contents to be committed to git by Wishlist
    """
    def __init__(self, wish):
        self.name = wish
        self.skel = C.skelpath + self.name + sep + "README.md"
        self.block = self._get_text()

    def __repr__(self):
        return self.name

    def _get_text(self) -> str:
        # hear ye, hear ye
        # wishlist.md is the source of truth
        # not prj_skel README            
        mdtext = ''
        with open(C.wishlist, 'r') as wl:
            _print_output = False
            _ct = 0
            for line in wl:
                if line.startswith('## ') and _print_output:
                    _print_output = False
                if _print_output:
                    _ct += 1
                    mdtext += line
                if line.startswith(f"## {self.name}"):
                    _ct += 1
                    _print_output = True
                    mdtext += line
        logger.debug(f"Got {_ct} lines for wish '{self.name}'.")
        return mdtext

    def del_wish(self) -> bool:
        # update wishlist
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
        # remove skel
        deldir = C.skelpath + self.name
        rmtree(deldir)

        # cleanliness
        self.block = None
        self.skel = None
        self.name = "." + self.name 
        return True

    def _print(self) -> None:
        print(self.block)

    def _write_block(self) -> bool:
        """
        Thought: CRUD operations can be generalized as a "write_block" operation
        so we could call open() in one place, here, instead of in every operation
        """
        pass
    def _make(self):
        """
        Add new Wish
        TODO: figure out proper way to open for editting via click
        It would be nice to not have click defined in Wish at all
        """
        block = \
    f"""    ## {self.name}
    ________
    ### Synopsis

    ### Usage

    ```
    {self.name}
    ```

    ### Would Require

    ### Difficulty


    """
        block = dedent(block)
        self.text = block

    def _edit(self):
        pass

    def _delete(self):
        pass


if __name__ == '__main__':
    wl = Wishlist()
    print(wl.wishes)
    w = Wish('useful')
    print(w.text)
    print(w.block)
