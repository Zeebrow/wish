import logging
import click
import make
import ls
import delete

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
    logger.debug("Starting")



cli.add_command(make.new_wish, name='make')
cli.add_command(ls.get_wishes, name='ls')
cli.add_command(ls.get_wish, name='get')
cli.add_command(delete.delete, name='del')

if __name__ == '__main__':
    cli()
