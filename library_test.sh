#!/bin/bash

mkdir -p library_tests_cache/
cp library_tests/*.py library_tests_cache/

RED='\033[0;31m'
RESET='\033[0m'
GREEN='\033[0;32m'

OK="${GREEN}OK${RESET}"
FAIL="${RED}FAIL${RESET}"

PSEUDO="pseudo/main.py"
PSEUDO_PYTHON="../pseudo-python/pseudo_python/main.py"

for path in library_tests_cache/*.py; do
  file="${path::-3}"

  printf "TEST $path\n"
  python3 $PSEUDO_PYTHON $path >> log 2>&1
  if [[ ! $? -eq 0 ]]; then
    printf "${FAIL} pseudo-python $path\n"
  else
    python3 $PSEUDO "$file.pseudo.yaml" py >> log 2>&1
    if [[ ! $? -eq 0 ]]; then
      printf "${FAIL} pseudo py $path\n"
    else
      output="$(python $file.py)"
      if [[ "$output" == "True" || "$output" == "true" ]]; then
        printf "${OK}   python\n"
      else
        printf "${FAIL} $output python\n"
      fi
    fi

    python3 $PSEUDO "$file.pseudo.yaml" rb >> log 2>&1
    if [[ ! $? -eq 0 ]]; then
      printf "${FAIL} pseudo rb $path\n"
    else
      output="$(ruby $file.rb)"
      if [[ "$output" == "True" || "$output" == "true" ]]; then
        printf "${OK}   ruby\n"
      else
        printf "${FAIL} $output ruby\n"
      fi
    fi

    python3 $PSEUDO "$file.pseudo.yaml" js >> log 2>&1
    if [[ ! $? -eq 0 ]]; then
      printf "${FAIL} pseudo js $path\n"
    else
      output="$(node $file.js)"
      if [[ "$output" == "True" || "$output" == "true" ]]; then
        printf "${OK}   javascript\n"
      else
        printf "${FAIL} $output javascript\n"
      fi
    fi

    pseudo "$file.pseudo.yaml" cs >> log 2>&1
    if [[ ! $? -eq 0 ]]; then
      printf "${FAIL} pseudo cs $path\n"
    else
      mcs $file.cs >> log 2>&1
      if [[ ! $? -eq 0 ]]; then
        printf "${FAIL} c# $file\n"
      else
        output="$($file.exe)"
        if [[ "$output" == "True" || "$output" == "true" ]]; then
          printf "${OK}   c#\n"
        else
          printf "${FAIL} $output c#\n"
        fi
      fi
    fi

    pseudo "$file.pseudo.yaml" go >> log 2>&1
    if [[ ! $? -eq 0 ]]; then
      printf "${FAIL} pseudo go $path\n"
    else
      output="$(go run $file.go 2>>log)"
      if [[ "$output" == "True" || "$output" == "true" ]]; then
        printf "${OK}   go\n"
      else
        printf "${FAIL} $output go\n"
      fi
    fi
  fi
done

