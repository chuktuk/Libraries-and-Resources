#!/bin/bash

DESTINATION=${2}"/"${1}

echo "Copying file ${1} to ${DESTINATION}" &&
gsutil cp ${1} ${DESTINATION} &&
rm ${1}
