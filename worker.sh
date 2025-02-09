#!/bin/bash

export RUN_VIA_BASH=True

# === Configuration ===
TOTAL_USERS=$1
TEST_TAG=$2
SPAWN_RATE=${3:-1}   # Default: 5 users/sec
RUN_TIME=${4:-1}     # Default: 1 min
FILE_SIZE=${5:-50}
ALL_USERS=${6:-true}

# Check required arguments
if [ -z "$TOTAL_USERS" ] || [ -z "$TEST_TAG" ] || [ -z "$FILE_SIZE" ]; then
    echo "Usage: $0 <total_users> <test_tag> [spawn_rate] [run_time] [file_size] [all_users]"
    exit 1
fi

# Set project paths
PROJECT_ROOT="$HOME/uyn_fw/locust"
LOG_DIR="$PROJECT_ROOT/logs"
mkdir -p "$LOG_DIR"  # Create log directory if it doesn't exist
LOG_FILE="$LOG_DIR/$(date +"%Y-%m-%d_%H-%M-%S")_${TOTAL_USERS}ccu_${TEST_TAG}.log"

# Move to project root
cd "$PROJECT_ROOT" || { echo "Error: Failed to change directory to $PROJECT_ROOT"; exit 1; }

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "Error: Virtual environment not found. Exiting."
    exit 1
fi

# Check if Locust is installed
if ! command -v locust &>/dev/null; then
    echo "Error: Locust is not installed in the virtual environment. Exiting."
    deactivate
    exit 1
fi

# === Start Performance Test ===
{
    echo "==================== Locust Test ===================="
    echo "Test Tag      : ${TEST_TAG}"
    echo "Total Users   : ${TOTAL_USERS}"
    echo "Spawn Rate    : ${SPAWN_RATE} users/sec"
    echo "Run Time      : ${RUN_TIME} minutes"
    echo "File Size     : ${FILE_SIZE}"
    echo "All Users Flag: ${ALL_USERS}"
    echo "Host          : https://storage.k8s.flodev.net"
    echo "Start Time    : $(date +"%Y-%m-%d %H:%M:%S")"

    SECONDS=0  # Track execution time

    locust --headless -f locustfile.py \
        --users="${TOTAL_USERS}" \
        --spawn-rate="${SPAWN_RATE}" \
        --run-time="${RUN_TIME}m" \
        --stop-timeout=300 \
        -T="${TEST_TAG}" \
        --all_users="${ALL_USERS}" \
        --size="${FILE_SIZE}" \
        --host="https://storage.k8s.flodev.net" \
        --only-summary

    duration=$SECONDS
    echo "End Time      : $(date +"%Y-%m-%d %H:%M:%S")"
    echo "Total Duration: $((duration / 60)) min $((duration % 60)) sec"
    echo "====================================================="
} >>"$LOG_FILE" 2>&1

# Deactivate virtual environment
deactivate

echo "All tests are finished. Log saved to: $LOG_FILE"
