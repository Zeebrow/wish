import logging
import tempfile
import click
import constants as C
import ls

logger = logging.getLogger(__name__)
# TODO make debug optional
# TODO: wish not saving on edit
#@click.option('debug')
@click.command()
@click.argument('wish')
def edit_wish(wish: str, quiet=True, debug=False):
    """
    Prints the markdown block associated with the specified wish.
    Exits 0 on success and 1 otherwise.

    Args:
        wish (str): [description]
        quiet (bool, optional): [description]. Defaults to True.
        debug (bool, optional): [description]. Defaults to False.

    Returns:
        [type]: [description]
    """
    print('edit wish')
    if wish not in ls._get_wishes():
        logger.warning(f"Wish not found: {wish}")
        return None
    # stores lines to be edited
    block = ''
    # Stores all lines before wish is found
    before_wish = ''
    # STores all lines after wish is found
    after_wish = ''
    with open(C.wishlist, 'r') as wl:
        # Append to different part of file based on state of these vars
        append_output=False
        b4 = True
        after = False

        for line in wl:
            if line.startswith(f'## ') and append_output:
                after = True
                append_output = False
            if append_output:
                print("--" + line.strip())
                block += line
            if line.startswith(f'## {wish}'):
                b4 = False
                append_output = True
                block += line
            if b4:
                before_wish += line
            if after:
                after_wish += line

    block = click.edit(block, require_save=True, extension='.md')
    if not block:
        logger.warning(f"Wish '{wish}' not created - changes were not saved.")
        return None
    debug_after_tmp = tempfile.mkstemp(text=True, dir='.', suffix='.tmp', prefix='after-wish')
    debug_before_tmp = tempfile.mkstemp(text=True, dir='.', suffix='.tmp', prefix='before-wish')
    debug_wish_tmp = tempfile.mkstemp(text=True, dir='.', suffix='.tmp', prefix='wish')

    if debug:
        with open(debug_before_tmp[1], 'w') as b, open('comb.tmp', 'w') as c:
            b.write(before_wish)
            c.write(before_wish)
        with open(debug_wish_tmp[1], 'w') as f, open('comb.tmp', 'a') as c:
            f.write(block)
            c.write(block)
        with open(debug_after_tmp[1], 'w') as a, open('comb.tmp', 'a') as c:
            a.write(after_wish)
            c.write(after_wish)
        #with open('comb.tmp', 'w') as c:
        #    c.write(before_wish)
        print(f"before wish debug file: {debug_before_tmp[1]}")
        print(f"wish debug file: {debug_wish_tmp[1]}")
        print(f"after wish debug file: {debug_after_tmp[1]}")


def _commit():
    # AHA. ha. lol
    pass
