cd $(dirname $BASH_SOURCE)/../
pwd
rm dist/*
python -m setuptools_scm
python -m build
twine upload -r ceba dist/*
twine upload -r pypi dist/*
