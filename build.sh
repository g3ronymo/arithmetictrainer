#!/usr/bin/sh
echo "This script assumes:"
echo "- the current working directory is the top level git directory of the"
echo "  arithmetictrainer repository"
echo ""
echo "Continue? [Y/n]"
read
if [ "$REPLY" = "n" ] || [ "$REPLY" = "N" ] || [ "$REPLY" = "no" ] || [ "$REPLY" = "No" ]
then
    exit 0
fi

# activate virtual environment
if [ ! -d ./venv ]
then 
    python -m venv .venv
fi
source .venv/bin/activate

# run tests
python -m unittest discover -v -s tests/


echo "------------------------------------------------------------------------"
echo build-docs
pip install --upgrade sphinx
pip install --upgrade furo
pip install --upgrade pyxdg
sphinx-build -b html docs/source docs/build/html/

echo "------------------------------------------------------------------------"
echo "build for pip"
pip install --upgrade build
python3 -m build

echo "------------------------------------------------------------------------"
echo "build zipapp"
if [ ! -d 'dist' ]
then 
    mkdir dist
fi
python3 -m zipapp arithmetictrainer -p '/usr/bin/env python3' -m 'cli:main'\
    -o dist/arithmetictrainer.pyz

