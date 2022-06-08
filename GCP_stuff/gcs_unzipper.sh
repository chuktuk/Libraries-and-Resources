#!/bin/bash

# . gcs_unzipper.sh gs://input/path gs://output/path
# creates unzipped (from .gz) versions of files in new path

FILES=$(gsutil ls ${1}/*.gz)

for f in $FILES
do
  NEW_FILE=${f//$1/$2}
  gsutil cat $f | zcat | gsutil cp - ${NEW_FILE//".gz"/""}
done
