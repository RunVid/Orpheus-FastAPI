#!/bin/bash

host=${1:-35.226.72.192}

# Ensure 'play' command is available
if ! command -v play &> /dev/null; then
    echo "Error: 'play' command not found. Please install 'sox' to play audio."
    exit 1
fi

echo "Requesting streaming speech..."

# Pipe the binary audio data directly to play without trying to process it with read
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "model": "orpheus",
    "input": "Uh...<groan> what...what the fuck are you talking about? I'\''m just doing a streaming llama three B text to speech test, you know?",
    "voice": "tara",
    "response_format": "wav",
    "speed": 1.0
  }' \
  http://$host:5005/v1/audio/speech/stream \
  --no-buffer \
  --silent \
  --output - | play -t wav - -q

echo "Streaming finished."