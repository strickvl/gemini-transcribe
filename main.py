import vertexai
from vertexai.generative_models import GenerativeModel, GenerationConfig, Part
from google.cloud import storage
from rich.console import Console
from rich.panel import Panel
from rich import print as rprint
import argparse
import os
from datetime import datetime

console = Console()

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Transcribe audio using Google Gemini")
parser.add_argument(
    "--input",
    type=str,
    default="Taking AI Agents to Production [bTlvrWeeqYo]_trimmed.mp3",
    help="Path to the audio file to transcribe",
)
parser.add_argument(
    "--model",
    type=str,
    default="gemini-2.0-flash-001",
    help="Gemini model to use (e.g., gemini-1.5-flash-002, gemini-2.0-flash-001)",
)
parser.add_argument(
    "--output",
    type=str,
    default=None,
    help="Path to save the transcription (defaults to input filename with .txt extension)",
)
args = parser.parse_args()

LOCAL_FILE_PATH = args.input

# Generate default output path if not specified
if args.output is None:
    base_filename = os.path.splitext(os.path.basename(LOCAL_FILE_PATH))[0]
    args.output = (
        f"{base_filename}_transcription_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    )

# TODO(developer): Update and un-comment below line
PROJECT_ID = "zenml-core"
GCP_REGION = "europe-north1"

console.print(Panel("Initializing Vertex AI", style="blue"))
vertexai.init(project=PROJECT_ID, location=GCP_REGION)

console.print(f"[bold cyan]Loading Gemini model: {args.model}...[/]")
model = GenerativeModel(args.model)

prompt = """
Can you transcribe this interview, in the format of timecode, speaker, caption.
Use speaker A, speaker B, etc. to identify speakers.
"""

# upload local file to GCS
bucket_name = "gemini-transcribe-test"

console.print(f"[bold yellow]Setting up GCS bucket: {bucket_name}[/]")
# create the bucket if it doesn't exist
client = storage.Client(project=PROJECT_ID)
if not client.bucket(bucket_name).exists():
    rprint(f"[bold green]Creating new bucket: {bucket_name}[/]")
    bucket = client.create_bucket(bucket_name, location=GCP_REGION)
    console.print(f"[green]Bucket {bucket_name} created in {bucket.location}[/]")
else:
    rprint(f"[blue]Using existing bucket: {bucket_name}[/]")
    bucket = client.bucket(bucket_name)

# Use the filename from LOCAL_FILE_PATH for the blob name
blob_name = os.path.basename(LOCAL_FILE_PATH)
console.print(
    f"[bold magenta]Uploading file: {LOCAL_FILE_PATH} → gs://{bucket_name}/{blob_name}[/]"
)
blob = bucket.blob(blob_name)
blob.upload_from_filename(LOCAL_FILE_PATH)
console.print("[green]✓ Upload complete[/]")

# Construct the GCS URI for the uploaded file
audio_file_uri = f"gs://{bucket_name}/{blob_name}"
console.print(f"[bold cyan]Preparing to transcribe audio from: {audio_file_uri}[/]")
audio_file = Part.from_uri(audio_file_uri, mime_type="audio/mpeg")

contents = [audio_file, prompt]

console.print(
    Panel(
        "Sending to Gemini for transcription... [italic](this may take a while)[/]",
        style="purple",
    )
)
response = model.generate_content(
    contents, generation_config=GenerationConfig(audio_timestamp=True)
)

console.print(Panel("Transcription Result", style="green"))
print(response.text)

# Save transcription to file
console.print(f"[bold green]Saving transcription to: {args.output}[/]")
with open(args.output, "w") as f:
    f.write(response.text)
console.print(f"[green]✓ Transcription saved successfully[/]")

# Example response:
# [00:00:00] Speaker A: Your devices are getting better over time...
# [00:00:16] Speaker B: Welcome to the Made by Google podcast, ...
# [00:01:00] Speaker A: So many features. I am a singer. ...
# [00:01:33] Speaker B: Amazing. DeCarlos, same question to you, ...
