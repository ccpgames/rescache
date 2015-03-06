import sys

if sys.platform == "darwin":
    from paths_mac import *
else:
    from paths_win import *
