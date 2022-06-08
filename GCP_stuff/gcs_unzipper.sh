#!/bin/bash

# usage
# . gcs_unzipper.sh gs://input/path gs://output/path PREFIX
# where PREFIX_ will be added to the beginning of each unzipped file 

FILES=$(gsutil ls ${1}/*.gz)
OLD_FILE_PREFIX=${1}"/"
NEW_FILE_PREFIX=${2}"/"${3}"_"

for f in $FILES
do
  NEW_FILE=${f//$OLD_FILE_PREFIX/$NEW_FILE_PREFIX}
  gsutil cat $f | zcat | gsutil cp - ${NEW_FILE//".gz"/""}
done
