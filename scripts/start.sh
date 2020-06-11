#!/bin/bash

python /initkg.py

supervisord -c /opt/run/supervisor.conf
