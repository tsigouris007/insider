#!/bin/sh

# Define default values for options
WORKDIR="/data"
TMPDIR="/tmp"
DEFAULT_OUTPUT_JSON="${WORKDIR}/report.json"
DEFAULT_OUTPUT_HTML="${WORKDIR}/report.html"
OUTPUT_FILE_JSON_O="${WORKDIR}/report.insider.original.json"
OUTPUT_FILE_JSON="${WORKDIR}/report.insider.json"
OUTPUT_FILE_HTML="${WORKDIR}/report.insider.html"

# Run the insider tool
insider "$@"

# Copy the report.html file to the host as is
mv $DEFAULT_OUTPUT_JSON "${OUTPUT_FILE_JSON}"
mv $DEFAULT_OUTPUT_HTML "${OUTPUT_FILE_HTML}"

# Format the json reports
python /report.py -i $OUTPUT_FILE_JSON -o $OUTPUT_FILE_JSON
