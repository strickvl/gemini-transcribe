# gemini-transcribe

A command-line tool that uses Google Gemini to transcribe audio files with timestamps and speaker identification.

## Features

- Transcribes audio files using Google Gemini's AI capabilities
- Automatically identifies different speakers and adds timestamps
- Outputs transcription to both console and text file
- Supports customizable model selection

## Prerequisites

- Python 3.8 or higher
- Google Cloud account with Vertex AI and Cloud Storage APIs enabled
- Google Cloud credentials configured

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/gemini-transcribe.git
   cd gemini-transcribe
   ```

2. Install the required dependencies:
   ```
   pip install google-cloud-storage vertexai rich
   ```

3. Set up Google Cloud credentials:
   ```
   export GOOGLE_APPLICATION_CREDENTIALS="path/to/your/credentials.json"
   ```

## Usage

Basic usage:
```
python main.py
```

This will use the default input file and model.

### Command-line Arguments

- `--input`: Path to the audio file to transcribe (default: "Taking AI Agents to Production [bTlvrWeeqYo]_trimmed.mp3")
- `--model`: Gemini model to use (default: "gemini-2.0-flash-001")
- `--output`: Path to save the transcription (defaults to input filename with timestamp)

Examples:
```
# Specify a different input file
python main.py --input my_podcast.mp3

# Use a different Gemini model
python main.py --model gemini-1.5-flash-002

# Save to a specific output file
python main.py --output my_transcript.txt
```

## Output Format

The transcription is formatted with timestamps, speaker identification, and captions:

```
[00:00:00] Speaker A: Your devices are getting better over time...
[00:00:16] Speaker B: Welcome to the Made by Google podcast...
```

The output is displayed in the console and saved to the specified text file.
