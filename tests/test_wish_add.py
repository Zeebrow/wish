import unittest
import wish

# Not sure how I should set certain constants, like location of wishlist.md,
# path to prj-skel/{wish}/README.md, etc.
# environment variables might could work


class TestWish(unittest.TestCase):    

    def setUp(self):
        self.test_repo_base = Path("./test_repo_path")
        self.wishlist_file = self.test_repo_base / "wishlist.md"
        self.prj_path = self.test_repo_base / "prj-skel"

    def tearDown(self):
        pass

