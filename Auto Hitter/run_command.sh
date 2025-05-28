#!/bin/bash

COMMAND="echo hi"

for i in {1..50}; do
    echo "Run #$i:"
    eval "$COMMAND"

    #avoid sleep after 50th term
    if [ "$i" -lt 50 ]; then

       # sleep defined
        SLEEP_TIME=$((60 + RANDOM % 241))
        echo "Sleeping for $((SLEEP_TIME / 60)) minute(s) and $((SLEEP_TIME % 60)) second(s)..."
        sleep "$SLEEP_TIME"
    fi
done
