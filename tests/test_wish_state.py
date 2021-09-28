import unittest
from random import randint
import shutil
from os.path import basename
from os import PathLike
from pathlib import Path
from wishlist import Wish, check_prj_readme

class TestCreateWish(unittest.TestCase):    

    def gen_temp_wishlist(self, identifier: str):
        """
        Generates a temporary wishlist (prj-skel directory and wishlist.md)
        by copying a template
        """
        tempdir_name = f"{identifier}_{randint(1000,9999)}_repo"
        # for when run from wish repo's home
        basedir = Path(__file__).parent.resolve()
        newdir = basedir / tempdir_name
        shutil.copytree(Path(basedir/"fixture_repo"), newdir)
        return newdir

    def setUp(self):
        """ """
        self.this_repo = self.gen_temp_wishlist(identifier="test_create")
        self.this_wishlist = self.this_repo / "wishlist.md"
        self.w1 = Wish("test1", repo_path=self.this_repo)
        self.w2 = Wish("test2", repo_path=self.this_repo)
        self.w3 = Wish("test3", repo_path=self.this_repo)
        self.w4 = Wish("test4bad_skel_no_match_wl", repo_path=self.this_repo)

    def test_wish_check_prj_readme(self):
        self.assertFalse(check_prj_readme(self.w4))
        self.assertTrue(check_prj_readme(self.w1))

    def tearDown(self):
        shutil.rmtree(self.this_repo)
        
    def test_wish_doesnt_exist_until_create(self):
        """Not an attribute test, since depends on success of create()"""
        new_w5 = Wish("new_wish_5", repo_path=self.this_repo)
        self.assertFalse(new_w5.exists)
        new_w5.create()
        self.assertTrue(new_w5.exists)

    def test_wish_attributes(self):
        return
        new_w5 = Wish("new_wish_5", repo_path=self.this_repo)
        self.assertEqual(new_w5.repo_path, self.this_repo)
        self.assertEqual(new_w5.prj_path, self.wish_prj_base_dir)
        self.assertEqual(new_w5.readme, self.wish_readme)
        self.assertIsInstance(new_w5.prj_path, PathLike)

if __name__ == '__main__':
    unittest.main()
