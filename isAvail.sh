#!/bin/sh

cat classrooms.txt \
  | grep -i "$1" \
  | python3 gridSearch.py
