"""Utility functions for file handling."""

import logging
import mimetypes
from pathlib import Path


def get_file_type(file_path):
    """
    Determine if a file is audio or video using MIME types.

    Args:
        file_path: Path to the file to check

    Returns:
        str or None: Returns 'audio', 'video', or None if type cannot be determined
    """
    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type:
        media_type = mime_type.split("/")[0]
        if media_type in ["audio", "video"]:
            return media_type
    return None


def get_input_path():
    """
    Interactively get a valid file or directory path from user.

    Returns:
        Path or None: Returns Path object if valid path provided, None if user quits
    """
    while True:
        path_input = input(
            "Enter the path to your audio/video file or directory (or 'q' to quit): "
        ).strip()

        if path_input.lower() == "q":
            return None

        # Remove quotes if present
        if (path_input.startswith("'") and path_input.endswith("'")) or (
            path_input.startswith('"') and path_input.endswith('"')
        ):
            path_input = path_input[1:-1]

        path = Path(path_input)
        if path.exists():
            return path
        logging.warning(f"The path '{path_input}' does not exist. Please try again.")
        return None
