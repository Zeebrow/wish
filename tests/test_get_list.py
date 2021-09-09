import unittest
import logging
from pathlib import Path
import wishlist
import subprocess

logger = logging.getLogger()
f = logging.Formatter('%(asctime)s : %(name)s : %(funcName)s : %(levelname)s: %(message)s')
sh = logging.StreamHandler()
sh.setFormatter(f)
logger.addHandler(sh)
logger.setLevel(logging.DEBUG)

class TestListWishes(unittest.TestCase):

    def setUp(self):
        subprocess.run(['./reset_test_setup'])
        self.test_repo_base = Path("./test_repo_path")
        self.wishlist_file = self.test_repo_base / "wishlist.md"
        self.prj_path = self.test_repo_base / "prj-skel"

        self.w_0 = wishlist.Wish("test1", repo_path=self.test_repo_base)

    def test_list_wishes(self):
        self.assertIsInstance(wishlist.get_wishes(wishlist_file=self.wishlist_file), list)
        self.assertEqual(wishlist.get_wishes(wishlist_file=self.wishlist_file)[0], "test1")

    def test_add_wish(self):
        self.assertEqual(len(wishlist.get_wishes(wishlist_file=self.wishlist_file)), 1)
        self.assertNotIn("new_wish_1", wishlist.get_wishes(wishlist_file=self.wishlist_file))
        
        w_new = wishlist.Wish("new_wish_1", repo_path=self.test_repo_base)
        print(w_new.block)
        w_new.create()
        self.assertIn("new_wish_1",wishlist.get_wishes(wishlist_file=self.wishlist_file))

if __name__ == '__main__':
    unittest.main()
