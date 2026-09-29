#!/usr/bin/env bash
set -e

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

# Deno JavaScript runtime for yt-dlp.
export DENO_INSTALL="${DENO_INSTALL:-$HOME/.deno}"
export PATH="$DENO_INSTALL/bin:$PATH"

if [ ! -x "$DENO_INSTALL/bin/deno" ] && command -v deno >/dev/null 2>&1; then
    DENO_BIN="$(command -v deno)"
else
    DENO_BIN="$DENO_INSTALL/bin/deno"
fi

if [ ! -x "$DENO_BIN" ]; then
    echo "ERROR: Deno JavaScript runtime is not installed."
    echo "Run ./install.sh first."
    exit 1
fi

if [ ! -d "$ROOT/venv" ]; then
    echo "ERROR: Python environment not found."
    echo "Run ./install.sh first."
    exit 1
fi

source "$ROOT/venv/bin/activate"

export LLM_PROVIDER=ollama
export OLLAMA_BASE_URL=http://127.0.0.1:11434/v1
export OLLAMA_MODEL=llama3.2:3b

if [ -d "/storage/emulated/0" ]; then
    OUTPUT_DIR="/storage/emulated/0/CLIPPER"
    PLATFORM="Android / DroidSpaces"
else
    OUTPUT_DIR="$HOME/CLIPPER"
    PLATFORM="Arch Linux Desktop"
fi

mkdir -p "$OUTPUT_DIR" output

if ! pgrep -x ollama >/dev/null 2>&1; then
    echo "[Ollama] Starting..."
    nohup ollama serve >/tmp/ollama.log 2>&1 &
    sleep 3
fi

clear

echo "=========================================="
echo "      AI YOUTUBE SHORTS GENERATOR"
echo "=========================================="
echo "Developer: Arkael-Dev"
echo "Platform : $PLATFORM"
echo "=========================================="
echo

echo "Select output resolution:"
echo
echo "  1) 720 x 1280"
echo "  2) 1080 x 1920"
echo
read -r -p "Choice [1]: " RES_CHOICE
RES_CHOICE="${RES_CHOICE:-1}"

case "$RES_CHOICE" in
    1)
        SOURCE_FORMAT="720"
        OUTPUT_WIDTH="720"
        OUTPUT_HEIGHT="1280"
        ;;
    2)
        SOURCE_FORMAT="1080"
        OUTPUT_WIDTH="1080"
        OUTPUT_HEIGHT="1920"
        ;;
    *)
        echo "Invalid resolution choice."
        exit 1
        ;;
esac

echo
echo "Select subtitle color:"
echo
echo "  1) White"
echo "  2) Yellow"
echo "  3) Cyan"
echo "  4) Green"
echo "  5) Pink"
echo "  6) Custom HEX"
echo
read -r -p "Choice [1]: " COLOR_CHOICE
COLOR_CHOICE="${COLOR_CHOICE:-1}"

case "$COLOR_CHOICE" in
    1) SUBTITLE_COLOR="FFFFFF" ;;
    2) SUBTITLE_COLOR="FFFF00" ;;
    3) SUBTITLE_COLOR="00FFFF" ;;
    4) SUBTITLE_COLOR="00FF66" ;;
    5) SUBTITLE_COLOR="FF66CC" ;;
    6)
        read -r -p "Enter HEX color (example FF8800): " SUBTITLE_COLOR
        SUBTITLE_COLOR="${SUBTITLE_COLOR#\#}"
        ;;
    *)
        echo "Invalid subtitle color choice."
        exit 1
        ;;
esac

if ! [[ "$SUBTITLE_COLOR" =~ ^[0-9A-Fa-f]{6}$ ]]; then
    echo "Invalid HEX color."
    exit 1
fi

export SHORTS_OUTPUT_WIDTH="$OUTPUT_WIDTH"
export SHORTS_OUTPUT_HEIGHT="$OUTPUT_HEIGHT"
export SUBTITLE_COLOR

echo
echo "Output     : ${OUTPUT_WIDTH}x${OUTPUT_HEIGHT}"
echo "Subtitles  : #${SUBTITLE_COLOR}"
echo "Background : blurred subtitle area"
echo
echo "Enter YouTube URL:"
read -r -p "> " URL

if [ -z "$URL" ]; then
    echo "URL cannot be empty."
    exit 1
fi

echo
echo "[1/1] Generating Shorts..."
echo

python main.py "$URL" \
    --mode local \
    --num-clips 1 \
    --aspect-ratio 9:16 \
    --format "$SOURCE_FORMAT" \
    --output-json output/result.json

echo
echo "=========================================="
echo " COPYING RESULTS"
echo "=========================================="

COUNT=0

for FILE in output/short_*.mp4; do
    [ -f "$FILE" ] || continue
    cp -f "$FILE" "$OUTPUT_DIR/"
    COUNT=$((COUNT + 1))
done

echo
echo "=========================================="
echo " COMPLETED"
echo "=========================================="
echo "Clips created : $COUNT"
echo "Output path   : $OUTPUT_DIR"
echo "Resolution    : ${OUTPUT_WIDTH}x${OUTPUT_HEIGHT}"
echo "Subtitle color: #${SUBTITLE_COLOR}"
echo

ls -lh "$OUTPUT_DIR"/short_*.mp4 2>/dev/null || true
