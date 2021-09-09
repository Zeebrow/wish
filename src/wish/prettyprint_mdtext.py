import os, sys, logging
from pathlib import Path
from subprocess import PIPE, STDOUT, Popen

from . import  constants as C

logger = logging.getLogger(__name__)

# First time depending on an external binary. Not sure how this will turn out.
# Could be a nightmare.
formatter = C.fmt_md_binary

def format_mdtext(mdtext=''):
    """
    Use Go binary to pretty-print markdown text
    """
    try:
        os.stat(formatter)
    except Exception:
        logger.warning(f"Could not stat formatter at '{formatter}', falling back to plaintext")
        print(mdtext)
        return

    # Leaving for if the need arises to print from file
#    if filename != '':
#        with open(readme, 'r') as md:
#            _mdtext = md.read().encode
#    else:
#        _mdtext = mdtext.encode()
    _mdtext = mdtext.encode()
    proc = Popen([formatter], stdin=PIPE)
    stdout_data = proc.communicate(input=_mdtext)


