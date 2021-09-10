import unittest
import random
import subprocess
from pathlib import Path
from wishlist import Wish
from wishlist import get_wishes

class TestWish(unittest.TestCase):    

    def setUp(self):
        # TODO: kinda janky - need better path resolution
        subprocess.run(["./reset_test_setup"])
        self.test_repo_base = Path("./test_repo_path")
        self.wishlist_file = self.test_repo_base / "wishlist.md"
    
    def tearDown(self):
        pass
    
    def _new_wish_name(self):
        n = random.randint(10,1000)
        name = f"./new_wish_{n}"
        prj_path = self.test_repo_base / "prj-skel" / Path(name)
        return name, prj_path
        
    # might could be two tests
    def test_add_wish(self):
        wish_name, prj_path = self._new_wish_name()

        w_new = Wish(
                wishname=wish_name,
                repo_path=self.test_repo_base)
        self.assertNotIn(wish_name, get_wishes(self.wishlist_file))
        w_new.create()
        self.assertIn(wish_name, get_wishes(self.wishlist_file))
        with open(prj_path /"README.md", 'r') as readme:
            mdtext = readme.read()
        self.assertEqual(w_new.block, mdtext)
        

    def test_edit_wish(self):
        wish_name, prj_path = self._new_wish_name()
        #wish_name = self._new_wish_name()
        #prj_path = self.test_repo_base / wish_name

        w_editme = Wish(
                wishname=wish_name, 
                repo_path=self.test_repo_base)
        w_editme.create()
        old_text = w_editme.block
        new_text = "ay es dee eff jay kay el semicolon"
        w_editme.update(new_text)
        self.assertNotEqual(old_text, new_text)

        with open(prj_path/"README.md", 'r') as readme:
            mdtext = readme.read()
        self.assertEqual(w_editme.block, mdtext)


if __name__ == '__main__':
    unittest.main()
