#!/bin/bash

source venv/bin/activate
gunicorn -w 4 -b 0.0.0.0:5000 studi:app --daemon
deactivate

