#!/usr/bin/env python

import os
import sys
from migrate.versioning.shell import main


if __name__ == '__main__':
    project_root = os.path.join(os.path.dirname(__file__), '..')
    sys.path.append(os.path.abspath(project_root))

    main(url='postgresql://postgres:postgres@localhost/devstream',
         debug='False', repository='devstream/migration')
