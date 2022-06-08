#!/bin/bash

FILES=$(gsutil ls ${1})

for f in $FILES
do
  gsutil cat $f | zcat | gsutil cp - ${f//".gz"/""}
  gsutil rm $f
done
