#!/bin/bash
#
# get_dremio_token.sh - Generate Dremio access token from username/password
#
# Usage:
#   ./get_dremio_token.sh <username> <password>
#   ./get_dremio_token.sh  # Prompts for credentials interactively
#
# Network Requirements:
#   - Port 9047 must be accessible on lakehouse-1.jgi.lbl.gov
#   - If blocked, use SSH tunnel: ssh -L 9047:lakehouse-1.jgi.lbl.gov:9047 gateway-host
#   - Or request firewall access from JGI network team
#
# Security Notes:
#   - This uses the v2 login API (internal use only)
#   - PAT feature not available until Dremio Enterprise upgrade
#   - Do NOT hardcode credentials in scripts or commit them to git
#   - Store token in DREMIO_PAT environment variable or secure vault
#
# Example:
#   export DREMIO_PAT=$(./get_dremio_token.sh myuser mypass)
#
# Reference: Georg Rath's script from JGI Slack
#

set -euo pipefail

# Configuration
DREMIO_HOST="${DREMIO_HOST:-lakehouse-1.jgi.lbl.gov}"
DREMIO_PORT="${DREMIO_PORT:-9047}"
DREMIO_LOGIN_URL="https://${DREMIO_HOST}:${DREMIO_PORT}/apiv2/login"

# Helper function to parse JSON (avoids jq dependency)
q() {
  python3 -c "import sys, json; print(json.load(sys.stdin)['$1'].strip())"
}

HOMEPATH=$(readlink -f ~/)
OUTFILE=$HOMEPATH"/.secrets/dremio_pat"

# Input validation
if [ $# -eq 0 ]; then
  # Interactive mode - will have the option to output the token to a file

  read -p "Output file where the token will be stored (default: ~/.secrets/dremio_pat, leave empty if you don't want to change): " OUTFILE_CHANGE
  read -p "Username: " USERNAME
  read -sp "Password: " PASSWORD
  echo
elif [ $# -eq 2 ]; then
  # Command-line arguments
  USERNAME="$1"
  PASSWORD="$2"
  OUTFILE_CHANGE=""
else
  echo "Error: Invalid arguments" >&2
  echo "Usage: $0 [username] [password]" >&2
  echo "   Or: $0  (for interactive prompt)" >&2
  exit 1
fi

# Validate inputs
if [ -z "$USERNAME" ] || [ -z "$PASSWORD" ]; then
  echo "Error: Username and password cannot be empty" >&2
  exit 1
fi

if ! [ -z "$OUTFILE_CHANGE"]; then
  echo "Changing the output file path to $OUTFILE_CHANGE"
  OUTFILE=$OUTFILE_CHANGE
fi


# Make API request
TEMP_FILE=$(mktemp)
trap "rm -f $TEMP_FILE" EXIT


# print the curl command for debugging purposes (without the password)
# echo "Running curl command: curl --silent --insecure --write-out \"%{http_code}\" --output $TEMP_FILE -X POST $DREMIO_LOGIN_URL --header 'Content-Type: application/json' --data-raw '{ \"userName\": \"$USERNAME\", \"password\": \"********\" }'"
HTTP_CODE=$(curl --silent --insecure \
  --write-out "%{http_code}" \
  --output "$TEMP_FILE" \
  -X POST "$DREMIO_LOGIN_URL" \
  --header 'Content-Type: application/json' \
  --data-raw "{
    \"userName\": \"$USERNAME\",
    \"password\": \"$PASSWORD\"
  }")

# Check response
if [ "$HTTP_CODE" -ne 200 ]; then
  echo "Error: Authentication failed (HTTP $HTTP_CODE)" >&2
  cat "$TEMP_FILE" >&2
  exit 1
fi

# Extract token
if ! TOKEN=$(cat "$TEMP_FILE" | q "token" 2>/dev/null); then
  echo "Error: Failed to parse token from response" >&2
  cat "$TEMP_FILE" >&2
  exit 1
fi

if [ -z "$TOKEN" ]; then
  echo "Error: Token is empty" >&2
  exit 1
fi

# Output token
echo "$TOKEN"

# Write if in the out file if a path was provided
if ! [ -z "$OUTFILE" ]; then
  # fullpath=$(readlink -f "$OUTFILE")
  # dir=$(dirname $fullpath)
  dir=$(dirname $OUTFILE)
  # echo $dir
  if [ ! -d $dir ] 
  then
    echo "creating the dir $dir"
    mkdir -p $dir
  fi
  echo "Exporting the token to $OUTFILE"
  echo "$TOKEN" > "$OUTFILE"
fi