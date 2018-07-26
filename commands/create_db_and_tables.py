import os
import sys

cwd = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, cwd)

if __name__ == '__main__':
    from gt.store.storage import create_database, create_tables

    create_database()
    create_tables()
