#!/bin/bash

if [[ $# -ne 1 ]]; then
    echo "Usage: $0 <num_runs>"
    exit 1
fi

run_code() {
    python testcase.py >/dev/null 2>&1
}

num_runs=$1

for ((i=1; i<=num_runs; i++)); do
    run_code &
done

wait
