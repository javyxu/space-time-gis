# first bump up package.json manually, commit and tag
cd ../..
python setup.py sdist
echo "RUN: twine upload dist/framework-{VERSION}.tar.gz"

