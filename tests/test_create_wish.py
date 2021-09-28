import unittest
from random import randint
import shutil
from os.path import basename
from os import PathLike
from pathlib import Path
from wishlist import Wish

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
        self.w4 = Wish("test4", repo_path=self.this_repo)

    def tearDown(self):
        shutil.rmtree(self.this_repo)
        
    def test_wish_doesnt_exist_until_create(self):
        """Not an attribute test, since depends on success of create()"""
        new_w5 = Wish("new_wish_5", repo_path=self.this_repo)
        self.assertFalse(new_w5.exists)
        new_w5.create()
        self.assertTrue(new_w5.exists)
    
    def test_create_raises_on_fail(self):
        """TODO
        Decide what constitutes 'failure to create wish' - fail to write file?
        fail to git commit?
        ???
        """
        pass

    def test_create_wish_name_is_configurable(self):
        """this might be a frivolous test"""
        rand_wishname = f"new_wish_{randint(1000,9999)}"
        new_w5 = Wish(rand_wishname, repo_path=self.this_repo)
        self.assertEqual(new_w5.name, rand_wishname)

    def test_wish_attributes(self):
        return
        """TODO: not exclusive to 'Wish().create()', needs to move"""
        new_w5 = Wish("new_wish_5", repo_path=self.this_repo)
        self.assertEqual(new_w5.repo_path, self.this_repo)
        self.assertEqual(new_w5.prj_path, self.wish_prj_base_dir)
        self.assertEqual(new_w5.readme, self.wish_readme)
        self.assertIsInstance(new_w5.prj_path, PathLike)

    def test_create_wish_name_equals_prj_skel_dir_name(self):
        """
        Changes to how directories and files are named should fail tests
        """
        new_w5 = Wish("new_wish_5", repo_path=self.this_repo)
        new_w5.create()
        self.assertEqual(new_w5.name, basename(new_w5.prj_path))

    def test_create_wish_creates_prj_skel(self):
        """Test for README.md"""
        wishname = "new_wish_5"
        new_w5 = Wish(wishname, repo_path=self.this_repo)
        self.assertFalse(Path(self.this_repo / "prj-skel" / wishname / "README.md").exists())
        new_w5.create()
        self.assertTrue(Path(self.this_repo / "prj-skel" / wishname / "README.md").exists())

    def test_created_wish_block_equals_prj_readme(self):
        new_w5 = Wish("new_wish_5", repo_path=self.this_repo)
        new_w5.create()
        with open(new_w5.readme, 'r') as md:
            self.assertEqual(new_w5.block, md.read())
    
    def test_create_wish_appends_to_wishlist_non_destructively(self):
        with open(self.this_wishlist, 'r') as wl:
            before_create = wl.read()
        new_w5 = Wish("new_wish_5", repo_path=self.this_repo)
        new_w5.create()
        with open(self.this_wishlist, 'r') as wl:
            after_create = wl.read()
        self.assertEqual(len(before_create), len(after_create) - len(new_w5.block))
    
    # def test_create_on_existing_wish_throws(self):
    #     self.assertTrue(False)

if __name__ == '__main__':
    unittest.main()
