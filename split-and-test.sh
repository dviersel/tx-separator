#!/usr/bin/env bash

# check if the file exists
if [ -f "$1" ]; then
  python3 transaction-separator.py $1

  # if no error occured
  if [ $? -eq 0 ]; then
    echo "File split successfully"

    cat ./transactions*.csv >> test.txt
    diff test.txt $1
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
