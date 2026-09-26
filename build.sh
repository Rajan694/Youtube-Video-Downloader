#!/usr/bin/env bash
set -e

TARGET="${1:-linux}"
TARGET=$(echo "$TARGET" | tr '[:upper:]' '[:lower:]')

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=== Building YouTube Downloader for target: $TARGET ==="

# Use a local virtual environment (system Python is externally managed)
VENV_DIR="$SCRIPT_DIR/.venv"
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment in .venv..."
    python3 -m venv "$VENV_DIR"
fi
source "$VENV_DIR/bin/activate"

echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt

if ! command -v pyinstaller &> /dev/null; then
    echo "PyInstaller not found. Installing..."
    pip install pyinstaller
fi

ICON_FLAG=""
if [ -f "yt.ico" ]; then
    ICON_FLAG="--icon=yt.ico --add-data=yt.ico:."
fi

case "$TARGET" in
    linux)
        echo "Building Linux executable..."
        pyinstaller --noconfirm --onefile --windowed --name "YouTubeDownloader" $ICON_FLAG main.py
        echo "Build complete: dist/YouTubeDownloader"
        ;;
    windows)
        echo "Building Windows executable..."
        if command -v wine &> /dev/null; then
            wine pyinstaller --noconfirm --onefile --windowed --name "YouTubeDownloader" --icon=yt.ico --add-data="yt.ico;." main.py
            echo "Build complete via Wine: dist/YouTubeDownloader.exe"
        else
            pyinstaller --noconfirm --onefile --windowed --name "YouTubeDownloader.exe" $ICON_FLAG main.py
            echo "Build finished: dist/YouTubeDownloader.exe"
        fi
        ;;
    *)
        echo "Unknown target: $TARGET. Allowed: linux, windows"
        exit 1
        ;;
esac
