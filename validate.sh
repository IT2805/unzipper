#!/usr/bin/env bash

traverse() {
  directory=$1

  # Iterate through all child directories and files
  for i in "$directory"/*; do

    # If directory, recursively move further down the directory tree
    if [ -d "$i" ]; then
      traverse "$i"

    # If file, execute the validation routine
    elif [ -f "$i" ]; then
      filename=$i

      # We only care about .html and .css files
      if [ "${filename: -5}" == ".html" ] ||
        [ "${filename: -4}" == ".css" ]; then

        # Split filename on dot [.], and extract the path without extension.
        # This assumes the path only has 1 dot [.] in it
        IFS='.' read -ra ADDR <<<"$filename"
        validate_file="${ADDR[0]}"_"${ADDR[1]}".json

        # Determine content type
        content_type=""
        if [ "${filename: -5}" == ".html" ]; then
          content_type="text/html"
        elif [ "${filename: -4}" == ".css" ]; then
          content_type="text/css"
        fi

        echo "> Posting file to W3 Validator"
        echo

        # It is extremely important to have the "@" before the filename
        curl -H "Content-Type: $content_type; charset=utf-8" \
          --data-binary @"$filename" \
          https://validator.w3.org/nu/?out=json >"$validate_file"

        echo
        echo "> Wrote response to ""$validate_file"""
        echo
      fi
    fi
  done
}

validate() {
  directory=$1
  traverse "$directory"
}

die() {
  echo "Illegal syntax! Make sure you use the following format:"
  echo "$ sh validate.sh assignment_directory"

  exit 1
}

# Valid syntax:
# $ sh validate.sh assignment_directory
[ "$#" -eq 1 ] || die

validate "$1"
