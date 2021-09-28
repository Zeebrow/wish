import unittest
from random import randint
import shutil
import os
from os.path import basename
from pathlib import Path
from wishlist import Wish, wish
from wishlist import get_wishes

class TestDeleteWish(unittest.TestCase):    
    
    """
    Assumes test_create_wish.py passes
    """

    # def gen_tempdir_name(self, identifier: str) -> str:
    #     return f"{identifier}_{randint(1000,9999)}"

    def gen_temp_wishlist(self, identifier: str):
        tempdir_name = f"{identifier}_{randint(1000,9999)}_repo"
        # for when run from wish repo's home
        basedir = Path(__file__).parent.resolve()
        newdir = basedir / tempdir_name
        shutil.copytree(Path(basedir/"fixture_repo"), newdir)
        return newdir

    def setUp(self):
        """ """
        self.this_repo = self.gen_temp_wishlist(identifier="test_delete")
        self.w1 = Wish("test1", repo_path=self.this_repo)
        self.w2 = Wish("test2", repo_path=self.this_repo)
        self.w3 = Wish("test3", repo_path=self.this_repo)
        self.w4 = Wish("test4", repo_path=self.this_repo)

        # self.wishlist = self.this_repo / "wishlist.md"
        # print(get_wishes(wishlist_file=self.wishlist))
        # self.w = Wish(wishname=self.wishname, 
        #        repo_path=self.this_repo)
        # self.wish_prj_base_dir = self.this_repo / "prj-skel" / self.wishname
        # self.wish_readme = self.wish_prj_base_dir / "README.md"

    def tearDown(self):
        pass
        #shutil.rmtree(self.this_repo)

    def test_del_wish_removes_prj_dir(self):
        self.assertTrue(self.w3.prj_path.exists())
        self.w3.delete()
        self.assertFalse(self.w3.prj_path.exists())


    def test_del_wish_doesnt_affect_other_wishes_in_wl(self):

        wishname = "some_wish"

        w0 = Wish(wishname=f"pre_{wishname}", repo_path=self.this_repo)
        w0.create()

        w1 = Wish(wishname=f"delme_{wishname}", repo_path=self.this_repo)
        w1.create()

        w2 = Wish(wishname=f"post_{wishname}", repo_path=self.this_repo)
        w2.create()

        deleted_block = w1.block
        w1.delete()
        with open(self.this_repo/"wishlist.md",'r') as wl:
            wl_as_string = wl.read()

        self.assertIn(w0.block, wl_as_string)
        self.assertNotIn(deleted_block, wl_as_string)
        self.assertIn(w2.block, wl_as_string)

    def test_del_wish_(self):
        pass


if __name__ == '__main__':
    unittest.main()
