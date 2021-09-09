import unittest
import wish

# Not sure how I should set certain constants, like location of wishlist.md,
# path to prj-skel/{wish}/README.md, etc.
# environment variables might could work


class TestWish(unittest.TestCase):    

    def setUp(self):
        self.w1 = wish.Wish(wishname="test1", wishlist="./wishlist.md")

    def tearDown(self):
        pass

    def test_invalid_names(self):
        pass

    def test_wish_dne_errors(self):
        wish_dne = wish.Wish(wishname="does_not_exist", wishlist="./wishlist.md")
        self.assertFalse(wish_dne.exists)
        self.assertRaises()


