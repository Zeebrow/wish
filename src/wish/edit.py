import logging
import click
import constants as C

logger = logging.getLogger(__name__)

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
#   try:
#       os.stat(C.skelpath + wish)
#       logger.debug(f"Stat '{C.skelpath + wish}'")
#   except Exception as e:
#       logger.watning(f"Could not stat '{C.skelpath + wish}': {e}")
    with open(C.wishlist, 'r') as wl:
        _print_output=False
        for line in wl:
            if line.startswith(f'## ') and _print_output:
                _print_output = False
            if _print_output:
                print(line.strip())
                # print(''.join(line.strip().split(' ')[1:]))
            if line.startswith(f'## {wish}'):
                _print_output = True
                print(line.strip())
