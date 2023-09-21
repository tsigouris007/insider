#!/bin/sh

# Define default values for options
WORKDIR="/data/"
DEFAULT_OUTPUT_JSON="${WORKDIR}report.json"
DEFAULT_OUTPUT_HTML="${WORKDIR}report.html"
OUTPUT_FILE_JSON="${WORKDIR}report.insider.json"
OUTPUT_FILE_HTML="${WORKDIR}report.insider.html"

# Run the insider tool
insider "$@"

# Copy the report.json file to the host
mv $DEFAULT_OUTPUT_JSON "${OUTPUT_FILE_JSON}"
mv $DEFAULT_OUTPUT_HTML "${OUTPUT_FILE_HTML}"
