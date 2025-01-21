"""
Audio Scribe
-----------------
A Python package for transcribing audio files with speaker diarization
using Whisper and Pyannote.
"""

from .transcriber import main
from .models import TranscriptionPipeline, AudioProcessor
from .config import TranscriptionConfig
from .auth import TokenManager
from .utils import DependencyManager, complete_path

__version__ = "0.1.5"

__all__ = [
    "main",
    "TranscriptionPipeline",
    "TranscriptionConfig",
    "AudioProcessor",
    "TokenManager",
    "DependencyManager",
    "complete_path",
]
