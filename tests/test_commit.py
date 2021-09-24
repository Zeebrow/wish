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
        self.w1 = Wish("test-commit-wish-1", repo_path=self.this_repo)
        self.w1.create()

    def tearDown(self):
        shutil.rmtree(self.this_repo)
        
    def test_commit_adds_target_repo(self):
        pass

if __name__ == '__main__':
    unittest.main()
