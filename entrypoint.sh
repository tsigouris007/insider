#!/bin/sh

# Define default values for options
WORKDIR="/home/user"
DEFAULT_OUTPUT_JSON="${WORKDIR}report.json"
DEFAULT_OUTPUT_HTML="${WORKDIR}report.html"

# Run the insider tool
insider "$@"
