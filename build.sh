#!/usr/bin/sh
echo "This script assumes:"
echo "- we are in the top level git directory of the arithmetictrainer repository"

echo "------------------------------------------------------------------------"
echo "build for pip"
python3 -m build

echo "------------------------------------------------------------------------"
echo "build zipapp"
python3 -m zipapp arithmetictrainer -p '/usr/bin/env python3' -m 'cli:main' -o dist/arithmetictrainer.pyz

