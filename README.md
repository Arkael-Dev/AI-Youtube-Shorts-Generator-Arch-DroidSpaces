# AI YouTube Shorts Generator — Arch DroidSpaces

Open-source AI YouTube Shorts Generator adapted for **Android + Termux + DroidSpaces + Arch Linux ARM (AArch64)**.

This project is based on and modifies open-source code from the original project:

https://github.com/SamurAIGPT/AI-Youtube-Shorts-Generator

This repository does not claim the original upstream code as its own. Credits remain with the original authors and open-source contributors.

## Features

- 🎬 Convert long YouTube videos into short clips
- 🤖 AI-powered highlight detection
- 🎤 Whisper transcription
- 📱 Vertical 9:16 output for YouTube Shorts, TikTok and Reels
- ✂️ Automatic clip selection and cropping
- 📦 JSON output support
- 🐧 Designed for Arch Linux ARM
- 📱 Tested for Android environments using Termux and DroidSpaces
- 🆓 Open source

## Environment

Recommended environment:

- Android
- Termux
- DroidSpaces
- Arch Linux ARM
- AArch64 / ARM64
- Python 3.10+
- FFmpeg
- Git

## Installation

### 1. Termux

    pkg update
    pkg upgrade
    pkg install git

### 2. Enter Arch Linux through DroidSpaces

Check architecture:

    uname -m

Expected:

    aarch64

Update Arch:

    sudo pacman -Syu

Install required packages:

    sudo pacman -S git python python-pip ffmpeg

### 3. Clone the repository

    git clone https://github.com/Arkael-Dev/AI-Youtube-Shorts-Generator-Arch-DroidSpaces.git
    cd AI-Youtube-Shorts-Generator-Arch-DroidSpaces

### 4. Create Python environment

    python -m venv venv
    source venv/bin/activate

Upgrade pip:

    python -m pip install --upgrade pip

Install dependencies:

    pip install -r requirements.txt

If available:

    pip install -r requirements-local.txt

## Usage

Run the generator with a YouTube URL:

    python main.py "https://www.youtube.com/watch?v=VIDEO_ID"

Local processing:

    python main.py "https://www.youtube.com/watch?v=VIDEO_ID" --mode local

Specify the number of clips:

    python main.py "https://www.youtube.com/watch?v=VIDEO_ID" --num-clips 5

Specify the aspect ratio:

    python main.py "https://www.youtube.com/watch?v=VIDEO_ID" --aspect-ratio 9:16

Save the result as JSON:

    python main.py "https://www.youtube.com/watch?v=VIDEO_ID" --output-json result.json

## Project

Repository:

https://github.com/Arkael-Dev/AI-Youtube-Shorts-Generator-Arch-DroidSpaces

Original upstream project:

https://github.com/SamurAIGPT/AI-Youtube-Shorts-Generator

## Attribution

This repository is an independent adaptation of an existing open-source project.

The original project, source code, architecture, and contributions remain credited to their respective authors and contributors.

Arkael-Dev maintains this repository adaptation for Android, Termux, DroidSpaces and Arch Linux ARM environments.

## License

This project follows the license of the original upstream project.

Please refer to the original repository and included license files for the applicable license terms.

---

Maintained by [arkael-dev](https://github.com/Arkael-Dev)
