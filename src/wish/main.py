import logging
import click
from wish import Wish
from wishlist import Wishlist
import constants as C

logger = logging.getLogger()
f = logging.Formatter('%(asctime)s : %(name)s : %(funcName)s : %(levelname)s: %(message)s')
sh = logging.StreamHandler()
sh.setFormatter(f)
logger.setLevel(level=logging.DEBUG)
logger.addHandler(sh)

@click.group()
def cli():
    """
    Keep track of your list of projects you want to do.

    Wishes are managed by reading to and writing from wishlist.md.
    When you make a wish, you provide the name for the command you want to make.
    You can optionally edit a block of markdown to provide more details on your idea.

    When the markdown file is saved, wishlist.md and the project skeleton directory are committed to git.

    \b
    TODO:
    -----
    - edit a wish you have saved to continue where you left off.
    - publish your wish as a simple, static html webpage
    - grant a wish to move it off of wishlist.md and onto magicking.md or whateve

    """

wl = Wishlist()

@click.command()
def ls():
    """
    list all current wishes
    """
    # TODO: format
    wl.get_wishes()
    [print(w, end=' ') for w in wl.wishes]
    print()

@click.command()
@click.argument('wishname')
def get(wishname):
    # TODO format
    print(wl.get_wish(wishname))

@click.command()
@click.argument('wishname')
def make(wishname):
    w = Wish(wishname)
    w.create()
    mdtext = click.edit(w.block, require_save=True, extension='.md')
    if not mdtext:
        logger.warning(f"Wish '{wishname}' not created - changes were not saved.")
        click.secho(f"Wish '{wishname}' not created - changes were not saved.", fg='yellow')
        return
    w.update(mdtext)
    click.secho(f"Commiting new wish: {wishname}", fg='green')
#@click.command()
#@click.argument('wish')
#def make(wish):
#    if wl.wish_exists(wish):
#        click.secho(f"Cannot create new wish '{wish}' - wish already exists!", fg='yellow')
#        # logger.warning(f"Cannot create new wish '{wish}' - wish already exists!")
#        return
#    # click.edit automatically opens a temp file and handles the rest
#    mdtext = click.edit(C.new_wish_skel(wish), require_save=True, extension='.md')
#    if not mdtext:
#        logger.warning(f"Wish '{wish}' not created - changes were not saved.")
#        return None
#    wl.add_wish(wish, mdtext)
#    wl.commit(wish)
#    click.secho(f"Commiting new wish: {wish}", fg='green')
cli.add_command(make, name='make')
cli.add_command(ls, name='ls')
cli.add_command(get, name='get')
# cli.add_command(delete.delete, name='del')
# cli.add_command(edit.edit_wish, name='edit')

if __name__ == '__main__':
    cli()
