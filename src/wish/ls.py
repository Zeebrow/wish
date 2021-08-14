import click
import logging
import constants as C

logger = logging.getLogger(__name__)

@click.command(short_help="Prints the list of wishes currently stored in wishlist.md and exits.")
@click.argument('fname')
def get_wishes(fname=C.wishlist):
    """
    Prints the list of wishes currently stored in wishlist.md and exits.

    Exits 0 on success and 1 otherwise.
    """
    click.echo(' '.join(wish for wish in _get_wishes()))

def _get_wishes():
    _wishes = []
    with open(C.wishlist, 'r') as wl:
        for line in wl:
            if line.startswith('## '):
                _wishes.append(''.join(line.strip().split(' ')[1:]))

    return _wishes


@click.command()
@click.argument('wish')
def get_wish(wish: str, quiet=True):
    """
    Prints the markdown block associated with the specified wish.
    Exits 0 on success and 1 otherwise.
    """
    if wish not in _get_wishes():
        logger.warning(f"Wish not found: {wish}")
        return None
    with open(C.wishlist, 'r') as wl:
        _print_output=False
        for line in wl:
            if line.startswith(f'## ') and _print_output:
                _print_output = False
            if _print_output:
                print(line.strip())
            if line.startswith(f'## {wish}'):
                _print_output = True
                print(line.strip())

