import constants as C

class WishList:
    def __init__(self, filename=C.wishlist) -> None:
        self.filename = filename

    def get_wishes(self) -> list:
        wishes = []
        with open(self.filename, 'r') as f:
            for line in f:
                if f.startswith('## '):
                    wishes.append(''.join(line.split(' ')[1:]))
        return wishes

class Wish:
    def __init__(self, wish) -> None:
        self.wish = wish
        self.exists = self.find()

    def find(self):
        with open(C.wishlist, 'r') as f:
            for line in f:
                if self.wish in line:
                    return True
        return False

    def delete(self):
        if self.exists:
            pass

    def create(self):
        pass

    def _commit_changes(self, repopath=C.repopath):
        pass

    def edit(self):
        if not self.exists:
            return
        pass

    def get(self):
        pass

    
