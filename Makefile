all: run

clean:
	rm -rf venv && rm -rf *.egg-info && rm -rf dist && rm -rf *.log*

venv:
	virtualenv --python=python3 venv && venv/bin/python setup.py develop

run: venv
	export FLASK_ENV=production && FLASK_APP=studi STUDI_SETTINGS=../settings.cfg venv/bin/flask run --host=0.0.0.0 --port=5000

test: venv
	STUDI_SETTINGS=../settings.cfg venv/bin/python -m unittest discover -s tests

sdist: venv test
	venv/bin/python setup.py sdist
