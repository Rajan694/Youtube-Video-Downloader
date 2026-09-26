# Youtube-Video-Downloader

A modern desktop application built with Python and Tkinter for downloading YouTube videos in high quality (MP4) or extracting audio (MP3) with live progress tracking, thumbnail previews, and metadata inspection.

## Features

- **Modern Dark UI:** YouTube-inspired dark theme with responsive controls.
- **Video & Audio Downloads:** Support for multiple resolutions (1080p, 720p, 480p, 360p) and MP3 audio extraction.
- **Live Metadata Preview:** Fetches video title, channel name, duration, view count, and thumbnail.
- **Progress Tracking:** Real-time progress bar with percentage and download speed.
- **Folder Chooser:** Choose custom download destination with system Downloads folder as default.
- **Cross-Platform Builds:** Ready-to-use build scripts for Linux and Windows executables via PyInstaller.

## Project Structure

```text
Youtube-Video-Downloader/
├── yt.ico             # Application icon
├── main.py            # Primary entry point
├── my youtube.py      # Legacy entry point wrapper
├── build.sh           # Linux/Bash build script
├── build.ps1          # Windows/PowerShell build script
└── src/
    ├── __init__.py    # Exports
    ├── config.py      # App constants, defaults, theme palette
    ├── downloader.py  # Asynchronous download engine (yt-dlp & pytube)
    ├── ui.py          # Tkinter interface, cards, progress bar
    └── utils.py       # Resource path resolution helper
```

## Running Locally

Requires Python 3.8+ and dependencies:

```bash
pip install yt-dlp pillow
python main.py
```

## Building Executables

### Linux (Bash)
```bash
chmod +x build.sh
./build.sh linux
```
Output: `dist/YouTubeDownloader`

### Windows (PowerShell)
```powershell
.\build.ps1 -Target windows
```
Output: `dist/YouTubeDownloader.exe`
