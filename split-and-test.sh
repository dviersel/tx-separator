#!/usr/bin/env bash

BASEDIR=$(pwd)

# check if the file exists
if [ -f "$1" ]; then

  # make directory based on basename
  BASENAME=$(basename "$1" | sed 's/\.[^.]*$//')
  RESULTS_DIR=$(pwd)/$BASENAME
  mkdir -p $RESULTS_DIR

  python3 transaction-separator.py $1 $RESULTS_DIR

  # if no error occured
  if [ $? -eq 0 ]; then
    echo "File split successfully"

    cd "$RESULTS_DIR" || exit

    cat transactions*.csv >> test.txt
    diff test.txt $BASEDIR/$1
    # if the file is the same as the original
    if [ $? -eq 0 ]; then
      echo "File is the same as the original"
      rm test.txt
    else
      echo "File is not the same as the original"
      echo "Error occured"
    fi
  fi
fi
