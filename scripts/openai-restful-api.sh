#!/bin/bash

host=${1:-35.226.72.192}

curl http://$host:5005/v1/audio/speech \
  -H "Content-Type: application/json" \
  -d '{
    "model": "orpheus",
    "input": "Uh...<groan> what...what the fuck are you talking about?",
    "voice": "tara",
    "response_format": "wav",
    "speed": 1.2
  }' \
  --output speech.wav
