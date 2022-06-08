#!/bin/bash

ZIPPED_FILENAME="${1}.gz"
DESTINATION="${2}/${ZIPPED_FILENAME}"

echo "gzipping and copying file ${1} to ${2}" &&
gzip ${1} &&
gsutil cp -v ${ZIPPED_FILENAME} ${DESTINATION} &&
rm ${ZIPPED_FILENAME}
