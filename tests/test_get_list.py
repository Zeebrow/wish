import unittest
import logging
from random import randint
import shutil
from pathlib import Path
from wishlist import get_wishes
from wishlist import Wish
import subprocess

logger = logging.getLogger()
f = logging.Formatter('%(asctime)s : %(name)s : %(funcName)s : %(levelname)s: %(message)s')
sh = logging.StreamHandler()
sh.setFormatter(f)
logger.addHandler(sh)
logger.setLevel(logging.DEBUG)

class TestListWishes(unittest.TestCase):
    
    """
    Assumes test_[create|del|update]_wish.py succeed
    """

    def new_test_wishname(self) -> str:
        return f"./test_wish_{randint(1000,9999)}"

    def make_fresh_wishlist(self, wishname: str):
        newdir = Path(wishname + "_repo")
        shutil.copytree(Path("./fixture_repo"), newdir)
        return newdir

    def setUp(self):
        self.wishname = self.new_test_wishname()
        self.this_repo = self.make_fresh_wishlist(
                wishname=self.wishname)
        self.wishlist = self.this_repo / "wishlist.md"

    def tearDown(self):
        shutil.rmtree(self.this_repo)

    def test_list_wishes(self):
        self.assertIsInstance(
                get_wishes(wishlist_file=self.wishlist), list)
        self.assertEqual(
                get_wishes(wishlist_file=self.wishlist)[0], "test1")

    def test_get_wishes_after_create_wish(self):
        w = Wish(wishname=self.wishname, repo_path=self.this_repo)
        self.assertNotIn("new_wish_1", get_wishes(wishlist_file=self.wishlist))
        w.create()
        self.assertIn(
                self.wishname, 
                get_wishes(wishlist_file=self.wishlist))

    def test_get_wishes_after_delete_wish(self):
        self.assertTrue(False)

    def test_get_wishes_after_edit_wish(self):
        self.assertTrue(False)

if __name__ == '__main__':
    unittest.main()
