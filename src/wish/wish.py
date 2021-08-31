import logging
from textwrap import dedent
from os.path import sep
import constants as C

import click

logger = logging.getLogger(__name__)

class Wishlist:
    def __init__(self):
        self.file = C.wishlist
        self.wishes = self._get_wishes()

    def _get_wishes(self):
        _wishes = []
        with open(C.wishlist, 'r') as wl:
            for line in wl:
                if line.startswith("## "):
                    w = ''.join(line.strip().split(' ')[1:])
                    _wishes.append(Wish(w))
        return _wishes

    def get_wish(self, wish):
        for w in self.wishes:
            if w.wish == wish:
                return w.text

        if wish not in self.wishes:
            click.echo(f"No such wish: {wish} - try wish make {wish} to create")
            return None

    def _add_wish(self, wish):
        w = Wish(wish)
        self.wishes.append(w)
        pass

class Wish:
    def __init__(self, wish):
        self.name = wish
        self.skel = C.skelpath + self.name + sep + "README.md"
        self.block = self._get_text()

    def __repr__(self):
        return self.name

    def __del__(self):
        # remove skel

        # update wishlist

        pass

    def _get_text(self):
        # hear ye, hear ye
        # wishlist.md is the source of truth
        mdtext = ''
        with open(C.wishlist, 'r') as wl:
            _print_output = False
            for line in wl:
                if line.startswith('## ') and _print_output:
                    _print_output = False
                if _print_output:
                    mdtext += line
                if line.startswith(f"## {self.name}"):
                    _print_output = True
                    mdtext += line

        return mdtext

    def _print(self):
        print(self.block)

    def _skel(self):
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

        return block

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
