AI YouTube Shorts Generator — Arch DroidSpaces

AI YouTube Shorts Generator for Android + Termux + DroidSpaces + Arch Linux ARM (AArch64).

Automatically turns YouTube videos into vertical Shorts with:

- AI highlight detection
- Local Ollama LLM
- Faster-Whisper transcription
- Automatic 9:16 reframing
- Automatic subtitles
- Subtitle color selection
- Blurred subtitle background
- 720×1280 or 1080×1920 output
- Automatic output to "CLIPPER"

Features

- 🎬 YouTube video → Shorts
- 🤖 Local AI highlight detection with Ollama
- 🎤 Local speech-to-text with Faster-Whisper
- ✂️ Automatic clip selection and cutting
- 📱 9:16 vertical video
- 💬 Automatic subtitles
- 🎨 Custom subtitle colors
- 🌫️ Blurred subtitle background
- ⚡ Designed for Arch Linux ARM / DroidSpaces
- 📦 Automatic dependency installation

Installation

Clone the repository:

```
git clone https://github.com/Arkael-Dev/AI-Youtube-Shorts-Generator-Arch-DroidSpaces.git
cd AI-Youtube-Shorts-Generator-Arch-DroidSpaces
```
Run the automatic installer:
```
./install.sh
```
The installer prepares the required environment, including:

- Python virtual environment
- Python dependencies
- FFmpeg
- DejaVu Sans
- Deno JavaScript runtime
- yt-dlp + yt-dlp-ejs
- Ollama
- "llama3.2:3b"
- Required local configuration

No manual Python dependency installation is required.

Usage

Start the generator:

./run.sh

Then select:

1. Output resolution
2. Subtitle color
3. YouTube URL

Example:

https://youtu.be/VIDEO_ID

The generated Shorts are automatically copied to:

/storage/emulated/0/CLIPPER

On a normal Arch Linux desktop, the output directory is:

~/CLIPPER

Requirements

Recommended:

- Android
- Termux
- DroidSpaces
- Arch Linux ARM / AArch64
- Internet connection for YouTube downloads
- Sufficient storage for video processing

The installer handles the required software and Python dependencies.

Credits

This project is an adaptation of:

https://github.com/SamurAIGPT/AI-Youtube-Shorts-Generator

Original authors and contributors remain credited according to the upstream project and its license.

This repository is maintained by Arkael-Dev for Android, Termux, DroidSpaces and Arch Linux ARM environments.

Repository

https://github.com/Arkael-Dev/AI-Youtube-Shorts-Generator-Arch-DroidSpaces

License

This project follows the applicable license of the original upstream project.

See the included "LICENSE" file and the upstream repository for license details.

---

Maintained by Arkael-Dev
