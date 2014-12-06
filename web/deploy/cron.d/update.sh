#!/bin/bash

CODE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )/../../" && pwd )"
BASE_DIR="$( cd "${CODE_DIR}/../" && pwd)"

if [ -e "${BASE_DIR}/data/updated" ]
then
	echo "updating"
	"${CODE_DIR}/update_data.sh"
	rm "${BASE_DIR}/data/updated"
else
	echo "not updating"
fi
