import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
from .db_manage import main


if __name__ == '__main__':
    main()
