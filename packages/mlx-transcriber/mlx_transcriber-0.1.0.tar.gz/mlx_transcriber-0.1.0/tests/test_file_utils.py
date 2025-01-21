"""Tests for file utility functions."""

from mlx_transcriber.utils.file_utils import get_file_type


def test_get_file_type():
    # Test audio files
    assert get_file_type("test.mp3") == "audio"
    assert get_file_type("test.wav") == "audio"
    assert get_file_type("test.m4a") == "audio"

    # Test video files
    assert get_file_type("test.mp4") == "video"
    assert get_file_type("test.avi") == "video"
    assert get_file_type("test.mov") == "video"

    # Test invalid files
    assert get_file_type("test.txt") is None
    assert get_file_type("test.pdf") is None
    assert get_file_type("test.xyz") is None
