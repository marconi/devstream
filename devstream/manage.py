#!/usr/bin/env python
from migrate.versioning.shell import main

if __name__ == '__main__':
    main(url='postgresql://postgres:postgres@localhost/devstream', debug='False', repository='migration')
