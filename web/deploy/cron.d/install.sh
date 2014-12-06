#!/bin/bash

BASEDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

cp "${BASEDIR}/pyp_update_data" /etc/cron.d/
echo "cron files installed"
