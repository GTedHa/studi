#!/bin/bash

kill -9 `ps aux | grep gunicorn | grep studi | awk '{ print $2 }'`
