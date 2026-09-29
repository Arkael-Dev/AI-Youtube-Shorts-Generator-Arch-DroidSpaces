# AI YouTube Shorts Generator — Arch Linux / DroidSpaces

AI-powered YouTube Shorts Generator for creating short-form videos from YouTube videos or local video files.

This repository is an adaptation for use on:

- Android
- Termux
- DroidSpaces
- Arch Linux ARM
- ARM64 / AArch64
- Python
- FFmpeg
- Local AI

The main code in this project is based on the original open-source project:

https://github.com/SamurAIGPT/AI-Youtube-Shorts-Generator

This repository does not claim the upstream code as originally created by Arkael-Dev. It uses and modifies the open-source code to make it more suitable for Android, Termux, DroidSpaces, and Arch Linux ARM environments.

---

## About the Project

This project takes long-form video and uses AI to identify potentially interesting sections, then generates short-form videos in a vertical format.

Output can be used for:

- YouTube Shorts
- TikTok
- Instagram Reels
- Other short-form video platforms

Main workflow:

    YouTube Video / Local Video
              ↓
         Transcription
              ↓
        AI Highlight Detection
              ↓
         Clip Selection
              ↓
          Vertical Crop
              ↓
            FFmpeg
              ↓
          Short Video

---

## Features

- 🎬 YouTube URL input
- 📁 Local video input
- 🤖 AI highlight detection
- 🎤 Whisper transcription
- ✂️ Automatic clip selection
- 📱 9:16 vertical video
- 🎯 Highlight ranking
- ♻️ Overlapping highlight deduplication
- 🧩 Long-video chunking
- 📦 JSON output
- 🧰 CLI
- 🐍 Python API
- 🎞️ FFmpeg video processing
- 📱 Android compatible
- 🐧 Arch Linux ARM compatible
- ⚙️ ARM64 / AArch64 compatible
- 🖥️ Designed to run through DroidSpaces
- 💻 Usable through Termux

---

## Environment

This repository is focused on the following workflow:

    Android
       ↓
    Termux
       ↓
    DroidSpaces
       ↓
    Arch Linux ARM
       ↓
    Python
       ↓
    AI + Whisper
       ↓
    FFmpeg
       ↓
    YouTube Shorts

Target architecture:

    aarch64

Check the architecture:

    uname -m

Expected output:

    aarch64

---

# Installation

## 1. Termux

Termux is used as the Android environment for running DroidSpaces.

Update packages:

    pkg update
    pkg upgrade

Install Git:

    pkg install git

Verify Git:

    git --version

After that, enter the Arch Linux environment through DroidSpaces.

---

## 2. Arch Linux ARM

After entering Arch Linux through DroidSpaces, check the architecture:

    uname -m

Expected:

    aarch64

Update the system:

    sudo pacman -Syu

If running as root:

    pacman -Syu

Install the basic dependencies:

    sudo pacman -S git python python-pip ffmpeg

If running as root:

    pacman -S git python python-pip ffmpeg

Verify:

    python --version
    pip --version
    git --version
    ffmpeg -version

---

## 3. Clone the Repository

Clone this repository:

    git clone https://github.com/Arkael-Dev/AI-Youtube-Shorts-Generator-Arch-DroidSpaces.git

Enter the project directory:

    cd AI-Youtube-Shorts-Generator-Arch-DroidSpaces

Check the project files:

    ls

---

## 4. Python Virtual Environment

Create a virtual environment:

    python -m venv venv

Activate it:

    source venv/bin/activate

Upgrade pip:

    python -m pip install --upgrade pip

Check Python:

    python --version

---

## 5. Install Python Dependencies

Install the main dependencies:

    pip install -r requirements.txt

If the project includes additional local dependencies:

    pip install -r requirements-local.txt

Use the requirements files included in the version of the repository you are using.

---

# AI Backend

The project uses the AI backend provided by the configuration and source code available in the repository.

For local workflows, the AI components can be used with a local environment compatible with ARM64.

If using Ollama as a local AI backend, verify that Ollama is available:

    ollama --version

Start the service:

    ollama serve

From another terminal:

    curl http://127.0.0.1:11434/api/tags

Install a model suitable for your device.

Example:

    ollama pull llama3.2

Check installed models:

    ollama list

Ollama endpoint:

    http://127.0.0.1:11434

Model and provider configuration must follow the implementation available in the repository source code.

---

# FFmpeg

FFmpeg is used for video processing and rendering.

Check FFmpeg:

    ffmpeg -version

Find the binary:

    which ffmpeg

If it is not installed:

    sudo pacman -S ffmpeg

---

# Whisper

Whisper is used for audio/video transcription.

For the local environment, transcription dependencies follow the project configuration.

The Whisper model can be selected according to the capabilities of the device.

Smaller models require fewer system resources.

On Android ARM64, transcription may take longer than on desktop systems with dedicated GPUs.

---

# Usage

## YouTube Video

Use a YouTube URL as the input:

    python main.py "https://www.youtube.com/watch?v=VIDEO_ID"

---

## Local Video

The project can also process local video files when local mode is supported by the source code.

Example:

    python main.py "/path/to/video.mp4" --mode local

Or:

    python main.py "file:///path/to/video.mp4" --mode local

Check available options:

    python main.py --help

---

# Generate Shorts

Example:

    python main.py "https://www.youtube.com/watch?v=VIDEO_ID" \
        --mode local \
        --num-clips 5 \
        --aspect-ratio 9:16

Shorts aspect ratio:

    9:16

Example resolution:

    1080x1920

On devices with limited resources, a lower resolution can be used according to the FFmpeg configuration.

---

# Python API

The upstream project provides a Python API through:

    from shorts_generator import generate_shorts

Example:

    result = generate_shorts(
        "/path/to/video.mp4",
        num_clips=5,
        aspect_ratio="9:16",
        mode="local",
    )

Then:

    for short in result["shorts"]:
        print(short["score"])
        print(short["title"])
        print(short["clip_url"])

The API and parameters follow the source code available in the repository.

---

# Batch Processing

Create:

    urls.txt

Put one YouTube URL on each line.

Example:

    https://www.youtube.com/watch?v=VIDEO_ID_1
    https://www.youtube.com/watch?v=VIDEO_ID_2
    https://www.youtube.com/watch?v=VIDEO_ID_3

Then run:

    xargs -a urls.txt -I{} python main.py "{}"

---

# CLI Options

CLI options follow the implementation available in the source code.

Common options include:

    --mode

Selects the processing mode.

    --num-clips

Sets the number of Shorts to generate.

    --aspect-ratio

Sets the output aspect ratio.

Example:

    --aspect-ratio 9:16

    --format

Sets the source quality/resolution.

Example:

    --format 720

    --language

Forces the transcription language.

Example:

    --language en

    --output-json

Saves the processing result as JSON.

Example:

    --output-json result.json

View all available options:

    python main.py --help

---

# Output

In local mode, generated videos can be stored in the output directory.

Example:

    output/

Example files:

    output/short_01.mp4
    output/short_02.mp4
    output/short_03.mp4

The exact output location follows the project configuration.

---

# Cache

Local transcription can use cached results so Whisper does not need to run again when a valid transcription already exists for the source video.

YouTube downloads may also use cached source files when caching is supported by the local project configuration.

This can reduce:

- Download time
- Bandwidth usage
- Transcription time
- CPU usage

---

# Highlight Detection

AI analyzes the transcript to identify potentially interesting sections.

Highlight criteria may include:

- Hook
- Emotional peak
- Opinion
- Revelation
- Conflict
- Quotable statement
- Story peak
- Practical value

Each highlight candidate may contain:

- Score
- Title
- Hook
- Reason
- Start time
- End time

The highlight algorithm follows the implementation of the open-source source code used by this project.

---

# Long Videos

Long videos can be processed using a chunking system.

Videos exceeding a configured duration can be divided into multiple sections with overlap.

This helps:

- Keep transcripts manageable
- Reduce the chance of missing highlights across chunk boundaries
- Allow AI to process long videos in smaller sections

Chunking parameters follow the project source code configuration.

---

# Smart Deduplication

When multiple highlight candidates overlap or are very close in time, the deduplication system can reduce duplicate or nearly identical Shorts.

This helps prevent generating multiple clips from essentially the same section.

---

# Vertical Crop

Horizontal videos can be converted into vertical videos.

Primary target:

    9:16

Suitable for:

- YouTube Shorts
- TikTok
- Instagram Reels

Cropping behavior follows the implementation available in the source code.

---

# JSON Output

The project can save analysis results as JSON when:

    --output-json

is used.

Example:

    python main.py "https://www.youtube.com/watch?v=VIDEO_ID" \
        --output-json result.json

The output may contain:

- Source video
- Transcript
- Highlight candidates
- Score
- Title
- Hook
- Virality reason
- Start time
- End time
- Output clip

The exact JSON structure follows the source code implementation.

---

# Configuration

Project configuration follows the configuration files and environment variables available in the repository.

Examples of local configuration variables that may be used by the source code:

    LLM_PROVIDER
    OPENAI_API_KEY
    OPENAI_MODEL
    GEMINI_API_KEY
    GEMINI_MODEL
    LOCAL_WHISPER_MODEL
    LOCAL_WHISPER_DEVICE
    LOCAL_OUTPUT_DIR

If an additional local AI backend such as Ollama is used, its configuration must follow the implementation available in the repository version being used.

Do not add environment variables that are not supported by the source code.

---

# Android / DroidSpaces Notes

This project is adapted to run the open-source source code in an Android environment through DroidSpaces.

Because Android devices have limited resources compared with desktop systems, pay attention to:

- RAM
- CPU
- Storage
- Device temperature
- Thermal throttling
- AI model size
- Video duration
- Output resolution

AI inference and video rendering can use significant CPU resources.

For devices with limited RAM:

- Use smaller AI models
- Use smaller Whisper models
- Reduce the number of clips
- Use a lower output resolution
- Avoid running multiple heavy processes simultaneously

---

# ARM64

Target environment:

    ARM64
    AArch64

Check:

    uname -m

Expected:

    aarch64

Not every Python dependency provides an ARM64 binary or wheel.

If a dependency does not provide an ARM64 wheel, pip may attempt to build it from source.

Building from source may require additional packages and may take longer.

---

# Project Structure

The project structure follows the source code being used.

Example:

    AI-Youtube-Shorts-Generator-Arch-DroidSpaces/
    ├── README.md
    ├── main.py
    ├── requirements.txt
    ├── requirements-local.txt
    ├── .env.example
    └── shorts_generator/
        ├── config.py
        ├── muapi.py
        ├── downloader.py
        ├── transcriber.py
        ├── highlights.py
        ├── clipper.py
        ├── pipeline.py
        └── local/
            ├── downloader.py
            ├── transcriber.py
            ├── llm.py
            └── clipper.py

The structure may change as the source code develops.

---

# Troubleshooting

## Ollama Connection

Check:

    ollama --version

Start:

    ollama serve

Then:

    curl http://127.0.0.1:11434/api/tags

---

## Model Not Found

Check:

    ollama list

Install a model:

    ollama pull llama3.2

---

## FFmpeg Not Found

Check:

    which ffmpeg

Install:

    sudo pacman -S ffmpeg

---

## Python Dependency Error

Make sure the virtual environment is active:

    source venv/bin/activate

Then:

    python -m pip install --upgrade pip

Install dependencies:

    pip install -r requirements.txt

---

## Permission Denied

Check:

    ls -la

If necessary:

    chmod +x filename

---

## Storage Full

Check:

    df -h

Check output size:

    du -sh output/

Remove old video files that are no longer needed.

---

# Performance

Performance depends on the device and configuration.

Factors include:

- CPU
- RAM
- AI model
- Whisper model
- Quantization
- Storage
- Video resolution
- Video duration
- FFmpeg
- Thermal throttling

Android ARM64 performance will vary from device to device and may differ significantly from desktop x86_64 systems or dedicated GPUs.

---

# Open Source Attribution

This project uses open-source source code from:

    https://github.com/SamurAIGPT/AI-Youtube-Shorts-Generator

The upstream source code is used as the foundation of this project and has been adapted for:

    Android
    Termux
    DroidSpaces
    Arch Linux ARM
    ARM64

The modifications in this repository are intended to adapt the installation, environment, configuration, and usage of the project for Android/Linux ARM devices.

Copyright notices and license terms from the upstream project remain applicable.

See the LICENSE file in this repository for the applicable license terms.

---

# Original Project

Original project:

    https://github.com/SamurAIGPT/AI-Youtube-Shorts-Generator

The upstream project provides the main implementation of the AI YouTube Shorts Generator.

This repository is an adaptation/modification for:

    Android
    Termux
    DroidSpaces
    Arch Linux ARM

---

# Credits

Special thanks to the developers and contributors of the open-source projects used as the foundation of this repository.

Original source:

    SamurAIGPT / AI-Youtube-Shorts-Generator

Open-source components used by the project may include:

- Python
- FFmpeg
- Whisper / faster-whisper
- OpenCV
- yt-dlp
- LLM providers
- Other open-source components listed in the source code and requirements

The credits and licenses of each respective project remain applicable.

---

# License

This repository uses and modifies open-source code.

The applicable license terms are those provided by the upstream source code and the respective dependencies.

Do not remove copyright notices or license information from the upstream source code.

For the complete license terms, see:

    LICENSE

Original project:

    https://github.com/SamurAIGPT/AI-Youtube-Shorts-Generator

---

# Repository

    https://github.com/Arkael-Dev/AI-Youtube-Shorts-Generator-Arch-DroidSpaces

---

# Author / Maintainer

    Arkael-Dev

This repository is maintained by Arkael-Dev as an adaptation and continued development of the AI YouTube Shorts Generator for Android, Termux, DroidSpaces, and Arch Linux ARM.

---

# Disclaimer

This project is provided for learning, experimentation, software development, automation, and content creation.

Users are responsible for:

- Videos they process
- Copyright of source videos
- Audio
- Images
- Footage
- AI models
- Generated content
- Use of generated videos
- Compliance with YouTube policies
- Compliance with the policies of other platforms

Make sure that all media and materials used have the appropriate rights or permissions.
