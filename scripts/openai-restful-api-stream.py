# openai-restful-api-stream.py
import requests
import json
import os
import argparse
from loguru import logger
from dotenv import load_dotenv

# Configure loguru logger
logger.remove()
logger.add(
    lambda msg: print(msg, flush=True, end=""),
    format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{message}</level>",
    colorize=True
)

# Load environment variables from .env file if it exists
load_dotenv()

# Get the base URL from environment variables or use a default
BASE_URL = os.environ.get("ORPHEUS_BASE_URL", "http://35.226.72.192:5005")
STREAM_URL = f"{BASE_URL}/v1/audio/speech/stream"

def stream_speech_from_orpheus(text: str, voice: str = "Orpheus", output_file: str = "stream.wav"):
    """Streams audio chunks from the Orpheus-FASTAPI server and saves to a WAV file."""
    headers = {
        'accept': 'audio/wav',  # Expecting WAV stream
        'Content-Type': 'application/json'
    }
    data = {
        'input': text,
        'voice': voice,
        'response_format': 'wav'  # Explicitly request WAV format
    }

    try:
        with open(output_file, 'wb') as f:
            with requests.post(STREAM_URL, headers=headers, json=data, stream=True) as response:
                response.raise_for_status()  # Raise an exception for bad status codes

                first_chunk = True
                for chunk in response.iter_content(chunk_size=8192):  # Iterate over data chunks
                    if first_chunk:
                        logger.info(f"Received initial chunk (likely WAV header) of length: {len(chunk)}")
                        first_chunk = False
                    elif chunk:
                        logger.info(f"Received audio chunk of length: {len(chunk)}")
                    else:
                        logger.info("Received empty chunk (end of stream?)")
                    
                    if chunk:
                        f.write(chunk)  # Write the chunk to file
            
        logger.info(f"Audio saved to {output_file}")

    except requests.exceptions.RequestException as e:
        logger.error(f"Error during streaming request: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Stream speech from Orpheus-FASTAPI server')
    parser.add_argument('--text', type=str, 
                       default="<groan> what...what the fuck are you talking about? I'm just doing a llama three B text to speech test, you know?",
                       help='Text to convert to speech')
    parser.add_argument('--voice', type=str, default="Orpheus",
                       help='Voice to use for speech synthesis')
    parser.add_argument('--output', type=str, default="stream.wav",
                       help='Output WAV file path')
    
    args = parser.parse_args()
    
    logger.info(f"Initiating streaming for text: '{args.text}' with voice: '{args.voice}'")
    stream_speech_from_orpheus(args.text, args.voice, args.output)
    logger.info("Streaming complete.")