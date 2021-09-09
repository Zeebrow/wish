import logging
import click
from ..wish import Wish, Wishlist, constants as C
#from wishlist import Wishlist
#import constants as C

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
@click.option('-r','--raw', 'raw', is_flag=True)
@click.argument('wishname')
def get(wishname, raw):
    w = Wish(wishname)
    w.pprint(raw)

@click.command()
@click.argument('wishname')
def edit(wishname):
    # TODO format
    logger.debug(f"Editting new wish: {wishname}...")
    click.secho(f"Editting wish: {wishname}", fg='green')
    w = Wish(wishname)
    mdtext = click.edit(w.block, require_save=True, extension='.md')
    if not mdtext:
        logger.warning(f"Wish '{wishname}' not created - changes were not saved.")
        click.secho(f"Wish '{wishname}' not created - changes were not saved.", fg='yellow')
        return
    w.update(mdtext)

@click.command()
@click.argument('wishname')
def make(wishname):
    logger.debug(f"Creating new wish: {wishname}...")
    click.secho(f"Creating new wish: {wishname}", fg='green')
    w = Wish(wishname)
    w.create()
    mdtext = click.edit(w.block, require_save=True, extension='.md')
    if not mdtext:
        logger.warning(f"Wish '{wishname}' not created - changes were not saved.")
        click.secho(f"Wish '{wishname}' not created - changes were not saved.", fg='yellow')
        return
    w.update(mdtext)

@click.command()
@click.argument('wishname')
def delete(wishname):
    logger.debug(f"Deleting wish: {wishname}...")
    click.secho(f"Deleting wish: {wishname}", fg='green')
    w = Wish(wishname)
    w.delete()


def commit_msg():
    pass

cli.add_command(make, name='make')
cli.add_command(ls, name='ls')
cli.add_command(get, name='get')
cli.add_command(delete, name='del')
cli.add_command(edit, name='edit')

if __name__ == '__main__':
    cli()
