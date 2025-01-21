#!/bin/bash

python setup.py sdist bdist_wheel
python setup_ag2.py sdist bdist_wheel
twine upload dist/*