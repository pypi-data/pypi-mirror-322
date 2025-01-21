"""Tests for the main transcriber CLI interface."""

import sys
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
from src.audio_scribe.transcriber import main


def test_main_delete_token(monkeypatch):
    """Test --delete-token command line option."""
    with patch("src.audio_scribe.transcriber.TokenManager") as mock_tm, patch(
        "src.audio_scribe.transcriber.DependencyManager"
    ) as mock_dm:

        # Setup mocks
        mock_tm_instance = MagicMock()
        mock_tm.return_value = mock_tm_instance
        mock_dm.verify_dependencies.return_value = True

        # Set command line args
        monkeypatch.setattr(sys, "argv", ["audio_scribe", "--delete-token"])

        # Run and verify
        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 0
        mock_tm_instance.delete_token.assert_called_once()


def test_main_dependency_check_fail(monkeypatch):
    """Test early exit on dependency check failure."""
    with patch("src.audio_scribe.transcriber.DependencyManager") as mock_dm:
        mock_dm.verify_dependencies.return_value = False

        monkeypatch.setattr(sys, "argv", ["audio_scribe"])

        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 1


def test_main_no_token(monkeypatch):
    """Test early exit when no token is provided."""
    with patch("src.audio_scribe.transcriber.DependencyManager") as mock_dm, patch(
        "src.audio_scribe.transcriber.get_token"
    ) as mock_get_token:

        mock_dm.verify_dependencies.return_value = True
        mock_get_token.return_value = None

        monkeypatch.setattr(sys, "argv", ["audio_scribe"])

        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 1


def test_main_model_init_failure(monkeypatch):
    """Test early exit on model initialization failure."""
    with patch("src.audio_scribe.transcriber.DependencyManager") as mock_dm, patch(
        "src.audio_scribe.transcriber.get_token"
    ) as mock_get_token, patch(
        "src.audio_scribe.transcriber.TranscriptionPipeline"
    ) as mock_pipeline:

        mock_dm.verify_dependencies.return_value = True
        mock_get_token.return_value = "fake-token"

        pipeline_instance = MagicMock()
        pipeline_instance.initialize_models.return_value = False
        mock_pipeline.return_value = pipeline_instance

        monkeypatch.setattr(sys, "argv", ["audio_scribe"])

        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 1
        pipeline_instance.initialize_models.assert_called_once_with("fake-token")


def test_main_successful_run(monkeypatch, tmp_dir):
    """Test successful end-to-end run."""
    test_audio = tmp_dir / "test.wav"
    test_audio.touch()

    with patch("src.audio_scribe.transcriber.DependencyManager") as mock_dm, patch(
        "src.audio_scribe.transcriber.get_token"
    ) as mock_get_token, patch(
        "src.audio_scribe.transcriber.TranscriptionPipeline"
    ) as mock_pipeline:

        # Setup all the mocks for success
        mock_dm.verify_dependencies.return_value = True
        mock_get_token.return_value = "fake-token"

        pipeline_instance = MagicMock()
        pipeline_instance.initialize_models.return_value = True
        pipeline_instance.process_file.return_value = True
        mock_pipeline.return_value = pipeline_instance

        # Set command line args
        monkeypatch.setattr(sys, "argv", ["audio_scribe", "--audio", str(test_audio)])

        # Run main
        main()

        # Verify
        pipeline_instance.initialize_models.assert_called_once()
        pipeline_instance.process_file.assert_called_once_with(test_audio)


def test_main_process_failure(monkeypatch, tmp_dir):
    """Test handling of processing failure."""
    test_audio = tmp_dir / "test.wav"
    test_audio.touch()

    with patch("src.audio_scribe.transcriber.DependencyManager") as mock_dm, patch(
        "src.audio_scribe.transcriber.get_token"
    ) as mock_get_token, patch(
        "src.audio_scribe.transcriber.TranscriptionPipeline"
    ) as mock_pipeline:

        mock_dm.verify_dependencies.return_value = True
        mock_get_token.return_value = "fake-token"

        pipeline_instance = MagicMock()
        pipeline_instance.initialize_models.return_value = True
        pipeline_instance.process_file.return_value = False
        mock_pipeline.return_value = pipeline_instance

        monkeypatch.setattr(sys, "argv", ["audio_scribe", "--audio", str(test_audio)])

        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 1


def test_main_interactive_audio_input(monkeypatch):
    """Test interactive audio file input."""
    with patch("src.audio_scribe.transcriber.DependencyManager") as mock_dm, patch(
        "src.audio_scribe.transcriber.get_token"
    ) as mock_get_token, patch(
        "src.audio_scribe.transcriber.TranscriptionPipeline"
    ) as mock_pipeline, patch(
        "builtins.input"
    ) as mock_input:

        mock_dm.verify_dependencies.return_value = True
        mock_get_token.return_value = "fake-token"

        pipeline_instance = MagicMock()
        pipeline_instance.initialize_models.return_value = True
        pipeline_instance.process_file.return_value = True
        mock_pipeline.return_value = pipeline_instance

        # Simulate user inputting file path
        mock_input.return_value = "/path/to/audio.wav"

        # Mock Path.exists to return True for our test path
        with patch.object(Path, "exists", return_value=True):
            monkeypatch.setattr(sys, "argv", ["audio_scribe"])
            main()

        pipeline_instance.process_file.assert_called_once_with(
            Path("/path/to/audio.wav")
        )


def test_main_show_warnings(monkeypatch):
    """Test --show-warnings flag behavior."""
    with patch("src.audio_scribe.transcriber.warnings") as mock_warnings, patch(
        "src.audio_scribe.transcriber.DependencyManager"
    ) as mock_dm:

        mock_dm.verify_dependencies.return_value = False

        monkeypatch.setattr(sys, "argv", ["audio_scribe", "--show-warnings"])

        with pytest.raises(SystemExit):
            main()

        mock_warnings.resetwarnings.assert_called_once()
