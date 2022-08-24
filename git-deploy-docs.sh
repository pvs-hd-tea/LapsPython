#!/bin/sh
touch docs/build/html/.nojekyll
git add -f docs/build/html
git commit -m "docs: update documentation"
git subtree push --prefix docs/build/html origin gh-pages
