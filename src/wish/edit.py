import logging
import click
import constants as C
import ls

logger = logging.getLogger(__name__)

@click.command()
@click.argument('wish')
def edit_wish(wish: str, quiet=True):
    """
    Prints the markdown block associated with the specified wish.
    Exits 0 on success and 1 otherwise.
    """
    print('edit wish')
    if wish not in ls._get_wishes():
        logger.warning(f"Wish not found: {wish}")
        return None
    block=''
    with open(C.wishlist, 'r') as wl:
        append_output=False
        for line in wl:
            if line.startswith(f'## {wish}'):
                print('match')
                append_output = True
                # block = block.join(line.strip())
                continue
            if line.startswith(f'## ') and append_output:
                append_output = False
            if append_output:
                print(line.strip())
                block = block.join(line.strip())
    print(block)
    block = click.edit(block, require_save=True, extension='.md')
    if not block:
        logger.warning(f"Wish '{wish}' not created - changes were not saved.")
        return None
    if debug:
        fname = tempfile.mkstemp(text=True, prefix=f"{wish}-", suffix=".tmp")
        print(f"fname: {fname}")
        with open(fname[1], 'w') as f:
            f.write(dedent(block))
    print('---')
    print(block)

