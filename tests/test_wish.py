import unittest
from random import randint
import shutil
from pathlib import Path
from wishlist import Wish
from wishlist import get_wishes

class TestWish(unittest.TestCase):    

    def new_test_wishname(self) -> str:
        return f"./test_wish_{randint(1000,9999)}"

    def make_fresh_wishlist(self, wishname: str):
        # random name for new wish
        # more convenient than tempfile or tempdir
        newdir = Path(self.new_test_wishname() + "_repo")
        print(f"copying to {newdir}")
        shutil.copytree(Path("./test_repo_path"), newdir)
        return newdir

    def setUp(self):
        self.wishname = self.new_test_wishname()
        print(self.wishname)
        self.this_repo = self.make_fresh_wishlist(
                wishname=self.wishname)
        print(self.this_repo)
        self.wishlist = self.this_repo / "wishlist.md"
        self.w = Wish(wishname=self.wishname, 
               repo_path=self.this_repo)
        print(self.wishname)
        self.wish_prj_base_dir = self.this_repo / "prj-skel" / self.wishname
        self.wish_readme = self.wish_prj_base_dir / "README.md"

    def tearDown(self):
        shutil.rmtree(self.this_repo)
    
    def test_create_wish(self):
        self.assertNotIn( self.wishname, get_wishes(wishlist_file=self.wishlist) )
        self.w.create()
        self.assertIn( self.wishname, get_wishes(wishlist_file=self.wishlist) )


if __name__ == '__main__':
    unittest.main()
