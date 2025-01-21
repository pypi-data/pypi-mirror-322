"""
Main entry point for Audio Scribe transcription tool.
Handles CLI interface and orchestrates the transcription process.
"""

import sys
import logging
import warnings
import argparse
import readline
from pathlib import Path
from datetime import datetime

from .config import TranscriptionConfig
from .models import TranscriptionPipeline
from .auth import TokenManager, get_token
from .utils import DependencyManager, complete_path

# Configure logging
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT,
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("transcription.log", mode="a", encoding="utf-8"),
    ],
)
logger = logging.getLogger(__name__)


def main():
    """Main entry point for the Audio Scribe CLI."""
    print(
        "Initializing environment... Please wait while we load dependencies and models."
    )
    sys.stdout.flush()

    parser = argparse.ArgumentParser(
        description="Audio Transcription Pipeline using Whisper + Pyannote, with optional progress bar."
    )
    parser.add_argument(
        "--audio", type=Path, help="Path to the audio file to transcribe."
    )
    parser.add_argument(
        "--token", help="HuggingFace API token. Overrides any saved token."
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Path to the output directory for transcripts and temporary files.",
    )
    parser.add_argument(
        "--delete-token",
        action="store_true",
        help="Delete any stored Hugging Face token and exit.",
    )
    parser.add_argument(
        "--show-warnings",
        action="store_true",
        help="Enable user warnings (e.g., from pyannote.audio). Disabled by default.",
    )
    parser.add_argument(
        "--whisper-model",
        default="base.en",
        help="Specify the Whisper model to use (default: 'base.en').",
    )
    args = parser.parse_args()

    # Manage user warnings
    if not args.show_warnings:
        warnings.filterwarnings(
            "ignore", category=UserWarning, module=r"pyannote\.audio"
        )
        warnings.filterwarnings("ignore", category=FutureWarning, module="whisper")
    else:
        warnings.resetwarnings()

    # Check dependencies
    if not DependencyManager.verify_dependencies():
        sys.exit(1)

    # Initialize tab-completion for file paths
    readline.set_completer_delims(" \t\n;")
    readline.set_completer(complete_path)
    readline.parse_and_bind("tab: complete")

    # Initialize the token manager
    token_manager = TokenManager()

    # If user wants to delete the stored token, do so and exit
    if args.delete_token:
        success = token_manager.delete_token()
        sys.exit(0 if success else 1)

    # Prepare configuration
    output_dir = args.output or (
        Path("transcripts") / datetime.now().strftime("%Y%m%d")
    )
    config = TranscriptionConfig(
        output_directory=output_dir, whisper_model=args.whisper_model
    )

    # Initialize pipeline
    pipeline = TranscriptionPipeline(config)
    hf_token = args.token or get_token(token_manager)
    if not hf_token:
        logger.error("No Hugging Face token provided. Exiting.")
        sys.exit(1)

    # Initialize models
    if not pipeline.initialize_models(hf_token):
        logger.error("Failed to initialize pipeline. Exiting.")
        sys.exit(1)

    # Prompt user for audio file path if not passed in
    audio_path = args.audio
    while not audio_path or not audio_path.exists():
        audio_path_str = input(
            "\nEnter path to audio file (Tab for autocomplete): "
        ).strip()
        audio_path = Path(audio_path_str)
        if not audio_path.exists():
            print(f"File '{audio_path}' not found. Please try again.")

    print("Audio file path accepted. Preparing to process the audio...")
    sys.stdout.flush()

    # Process the audio file
    if not pipeline.process_file(audio_path):
        sys.exit(1)


if __name__ == "__main__":
    main()
