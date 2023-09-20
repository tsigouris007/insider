#!/bin/sh

# Define default values for options
WORKDIR="/"
DEFAULT_OUTPUT_JSON="${WORKDIR}report.json"
DEFAULT_OUTPUT_HTML="${WORKDIR}report.html"
OUTPUT_FILE_JSON="/data/report.insider.json"
OUTPUT_FILE_HTML="/data/report.insider.html"

# Run the insider tool
insider "$@"

echo "Writing to ${OUTPUT_FILE}"

# Copy the report.json file to the host
cp $DEFAULT_OUTPUT_JSON "${OUTPUT_FILE_JSON}"
cp $DEFAULT_OUTPUT_HTML "${OUTPUT_FILE_HTML}"
