#!/bin/bash

# build
rm -rf build dist winwin.egg-info
python setup.py sdist bdist_wheel

# upload pypi.org [--verbose]
# uasename: winwin
# password: @赵斌
python -m twine upload dist/* &&
  echo "INFO: upload [pypi.org] success!!!"

# upload winwin.pypi to sys3007:/home/deploy/pypi/packages/
scp -P 2222 dist/* deploy@localhost:/home/deploy/pypi/packages/ &&
  echo "INFO: upload [sys3007-pypi] success!!!"
