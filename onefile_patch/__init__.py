"""
!!!Attention!!!
This module is a Patch for OneFile mode of Nuitka.
There is a difference between sys.argv[0] and __file__ of the main module for the onefile mode,
which is caused by using a bootstrap to a temporary location. Data files will be in the later location.
It makes that os.path.abspath(".") cannot return the absolute path of __main__.py to read the data inside.
See https://nuitka.net/user-documentation/common-issue-solutions.html#onefile-finding-files for more details.
"""

import os

# do not move this file or folder ,or modify MAIN_RUN_DIR
MAIN_RUN_DIR = os.sep.join(__file__.split(os.sep)[0:-2])