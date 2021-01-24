coverage run -m unittest discover -s ./tests/unit -t ./
#coverage report --omit="*/test*,venv/*,vendor/*"
#coverage html --omit="*/test*,venv/*,vendor/*" -d ./target/unit/coverage_html/
coverage report
coverage xml
coverage html
echo 'results generated in ./target/unit/coverage_html/'