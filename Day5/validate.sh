#!/bin/bash 
# shebang line

LOGFILE="logs/validate.log"
mkdir -p "$(dirname "$LOGFILE")"
#dirname "$LOGFILE" extracts the folder path from the log file (logs/).
#mkdir -p creates that folder if it doesn’t exist yet. 


# helper for timestamped log
log() {
  echo "$(date '+%Y-%m-%d %H:%M:%S') - $*" | tee -a "$LOGFILE"
}
#$* → represents all arguments passed to the log function
#tee -a "$LOGFILE" → prints the message to the screen and appends it (-a) to the log file at the same time.

log "Starting validation..."

# Check if src/ exists
if [ ! -d "src" ]; then
  log "ERROR: 1 src/ directory missing"
  exit 1
fi

# Check if config.json exists and is valid JSON
if [ ! -f "config.json" ]; then
  log "ERROR: 2 config.json not found"
  exit 2
fi

# Runs Python’s built-in JSON validator: python3 -m json.tool < config.json
# It reads the file (< config.json); Parses it as JSON; Prints formatted output if valid ; Returns an error if invalid
# >/dev/null 2>&1 → hides all output (both stdout and stderr).

if ! python3 -m json.tool < config.json >/dev/null 2>&1; then
  log "ERROR: 3 config.json is not valid JSON"
  exit 3
fi


log "Validation successful "
exit 0
