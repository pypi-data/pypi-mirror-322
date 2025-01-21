# MLX Transcriber

A user-friendly Python wrapper around MLX Whisper that simplifies audio and video transcription on Apple Silicon Macs.

## Features

- Easy-to-use interface for MLX Whisper transcription
- Automatic audio/video file type detection and conversion
- Batch processing of entire directories
- Automatic output file management
- Robust error handling and logging
- Automatic language detection (via MLX Whisper)
- Translation support (via MLX Whisper)
- Word-level timestamp support (via MLX Whisper)
- Optimized for Apple Silicon Macs using MLX

## Requirements

- macOS running on Apple Silicon (M1/M2/M3)
- Python 3.10 or 3.11
- FFmpeg installed on your system (`brew install ffmpeg`)
- MLX (installed automatically)

## Installation

### Quick Install (from PyPI)
```bash
pip install mlx-transcriber
```

### Development Install
1. Clone the repository:
```bash
git clone https://github.com/cavit99/mlx-transcriber.git
cd mlx-transcriber
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate
```

3. Install in development mode with test dependencies:
```bash
pip install ".[dev]"
```

## Building and Running Locally

1. First, ensure you have FFmpeg installed:
```bash
brew install ffmpeg
```

2. Clone and set up the project:
```bash
# Clone the repository
git clone https://github.com/cavit99/mlx-transcriber.git
cd mlx-transcriber

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate

# Install in editable mode with all dependencies
pip install -e ".[dev]"
```

3. Run the transcriber:
```bash
# Using the CLI command
mlx-transcribe

# Or using the Python module
python -m mlx_transcriber

# Or from Python
python
>>> from mlx_transcriber import transcribe_audio_or_video
>>> text = transcribe_audio_or_video("path/to/your/audio.mp3")
```

4. Run tests (optional):
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=mlx_transcriber
```

Note: The first time you run the transcriber, it will download the MLX Whisper model (about 3GB). This is a one-time download.

## Usage

### Command Line
After installation, you can run the transcriber directly from the command line:
```bash
mlx-transcribe
```

Or using the module:
```bash
python -m mlx_transcriber
```

The tool will:
1. Prompt for an audio/video file or directory path
2. Automatically detect and convert media files
3. Process transcription using MLX Whisper
4. Save transcriptions as text files with organized naming

### Python API
```python
from mlx_transcriber import transcribe_audio_or_video

# Transcribe a single file
text = transcribe_audio_or_video("audio.mp3")

# Process a directory
from mlx_transcriber import process_directory
process_directory("path/to/media/files")
```

### Supported File Types

Audio:
- MP3
- WAV
- M4A
- AAC
- FLAC

Video:
- MP4
- AVI
- MOV
- MKV
- WebM

## Development

### Running Tests
```bash
pytest
```

### Running Tests with Coverage
```bash
pytest --cov=mlx_transcriber
```

## Architecture

MLX Transcriber is designed as a user-friendly wrapper around MLX Whisper, focusing on:
- Simplified file handling and conversion
- Batch processing capabilities
- Organized output management
- Error handling and logging

The core transcription functionality is provided by MLX Whisper, while we handle the user experience layer.

## License

MIT License

## Credits

This project builds upon:
- [MLX Whisper](https://github.com/ml-explore/mlx-examples) - Apple's MLX implementation of Whisper, providing the core transcription functionality
- [python-ffmpeg](https://github.com/jonghwanhyeon/python-ffmpeg) - Python FFmpeg wrapper for media file handling 