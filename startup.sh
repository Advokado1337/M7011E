#!/bin/sh

# Determine path separator based on OS
if [ "$(uname)" = "Linux" ] || [ "$(uname)" = "Darwin" ]; then
    SEP=":"
else
    SEP=";"
fi

# Define the migrations directory
DIR=app/migrations/
if [ -d "$DIR" ]; then
    echo "Removing Lock ($DIR)"
    rm -rf "$DIR"
fi

echo "Clearing unused Docker resources..."
docker system prune -a -f

echo "Starting Docker Compose with build..."
docker-compose up --build
