"""MLX Transcriber - Audio and video transcription using MLX Whisper.

A user-friendly wrapper that adds file handling, batch processing, and CLI features
around MLX Whisper. Automatically handles audio/video conversion, supports directory
processing, and manages file output.

Features:
    - Automatic audio/video file type detection and conversion
    - Directory batch processing
    - User-friendly CLI interface
    - Automatic transcription file management
    - Error handling and logging

Usage:
    # Run as script
    python -m mlx_transcriber

    # Use as library
    from mlx_transcriber import transcribe_audio_or_video
    text = transcribe_audio_or_video("audio.mp3")
"""

import logging
import tempfile
import warnings
from pathlib import Path

import mlx_whisper
from ffmpeg import FFmpeg

from .utils.file_utils import get_file_type, get_input_path

# Configuration
TRANSCRIPTION_MODEL = "mlx-community/whisper-large-v3-mlx"
LOGGING_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"

# Set up logging
logging.basicConfig(level=logging.INFO, format=LOGGING_FORMAT)

# Suppress warnings
warnings.filterwarnings("ignore", category=UserWarning, module="urllib3")


def transcribe_audio_or_video(
    file_path, language=None, task="transcribe", word_timestamps=False
):
    """
    Transcribe audio/video with additional options

    Args:
        file_path: Path to audio/video file
        language: Optional language code (auto-detected if None)
        task: 'transcribe' or 'translate'
        word_timestamps: Whether to include word-level timestamps
    """
    try:
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"The file {file_path} does not exist.")

        file_type = get_file_type(str(file_path))
        if file_type not in ["audio", "video"]:
            msg = f"Unsupported file type: {file_type}."
            msg += " Please provide an audio or video file."
            raise ValueError(msg)

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_audio_path = Path(temp_dir) / "temp_audio.wav"

            logging.info(
                f"Processing {'video' if file_type == 'video' else 'audio'} file..."
            )
            ff = (
                FFmpeg()
                .option("y")  # Overwrite output file if it exists
                .input(str(file_path))
                .output(str(temp_audio_path), acodec="pcm_s16le", ar=16000, ac=1)
            )

            ff.execute()

            logging.info("Transcribing...")
            result = mlx_whisper.transcribe(
                str(temp_audio_path),
                path_or_hf_repo=TRANSCRIPTION_MODEL,
                language=language,
                task=task,
                word_timestamps=word_timestamps,
                verbose=True,
                # Optimized greedy decoding parameters
                temperature=0.0,  # Use greedy decoding
                compression_ratio_threshold=1.8,  # Stricter compression to prevent repetition
                condition_on_previous_text=True,  # Use context from previous text
                logprob_threshold=-0.7,  # Higher threshold for token probabilities
                no_speech_threshold=0.8,  # Stricter silence detection
                without_timestamps=not word_timestamps,  # Only use timestamps when requested
            )

        return result["text"]
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    return None


def process_directory(directory_path):
    """
    Process all audio and video files in a directory for transcription.

    Args:
        directory_path: Path to directory containing audio/video files

    Note:
        Creates {filename}_transcription.txt for each valid media file
    """
    directory = Path(directory_path)
    if not directory.is_dir():
        logging.error(f"'{directory_path}' is not a valid directory.")
        return

    audio_video_files = [
        f for f in directory.iterdir() if get_file_type(str(f)) in ["audio", "video"]
    ]

    if not audio_video_files:
        logging.warning(f"No audio or video files found in {directory_path}")
        return

    logging.info(f"Found {len(audio_video_files)} audio/video files to process")
    for file_path in audio_video_files:
        logging.info(f"\nProcessing: {file_path.name}")
        transcribed_text = transcribe_audio_or_video(file_path)

        if transcribed_text:
            output_file_path = file_path.with_suffix(".txt").with_stem(
                f"{file_path.stem}_transcription"
            )
            try:
                output_file_path.write_text(transcribed_text, encoding="utf-8")
                logging.info(f"Transcription saved to {output_file_path}")
            except Exception as e:
                logging.error(f"Error saving transcription for {file_path.name}: {e}")
        else:
            logging.error(f"Transcription failed for {file_path.name}")


def main():
    """Run the interactive CLI for transcription."""
    while True:
        input_path = get_input_path()
        if input_path is None:
            break

        if input_path.is_dir():
            process_directory(input_path)
        else:
            # Single file processing
            file_type = get_file_type(str(input_path))
            if file_type not in ["audio", "video"]:
                logging.error(
                    "Unsupported file type. Please provide an audio or video file."
                )
                continue

            transcribed_text = transcribe_audio_or_video(input_path)
            if transcribed_text:
                output_file_path = input_path.with_suffix(".txt").with_stem(
                    f"{input_path.stem}_transcription"
                )
                try:
                    output_file_path.write_text(transcribed_text, encoding="utf-8")
                    logging.info(f"Transcription saved to {output_file_path}")
                except Exception as e:
                    logging.error(
                        f"An error occurred while saving the transcription: {e}"
                    )
            else:
                logging.error("Transcription failed.")

        process_another = (
            input("Do you want to transcribe another file/directory? (y/n): ")
            .strip()
            .lower()
        )
        if process_another != "y":
            break

    logging.info("Thank you for using the transcription tool!")


if __name__ == "__main__":
    main()
