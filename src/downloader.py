import os
import threading
from urllib.request import urlopen
from io import BytesIO
from PIL import Image

class DownloaderEngine:
    def __init__(self):
        self.current_info = None

    def fetch_info_async(self, url: str, on_success, on_error):
        def _worker():
            try:
                info = self._fetch_metadata(url)
                self.current_info = info
                on_success(info)
            except Exception as e:
                on_error(f"Failed to fetch video: {str(e)}")

        threading.Thread(target=_worker, daemon=True).start()

    def _fetch_metadata(self, url: str) -> dict:
        # Prefer yt-dlp
        try:
            import yt_dlp
            ydl_opts = {"quiet": True, "no_warnings": True, "skip_download": True}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                meta = ydl.extract_info(url, download=False)
                return {
                    "url": url,
                    "title": meta.get("title", "Unknown Title"),
                    "author": meta.get("uploader", "Unknown Channel"),
                    "duration": meta.get("duration", 0),
                    "views": meta.get("view_count", 0),
                    "thumbnail_url": meta.get("thumbnail", ""),
                    "formats": ["Best Quality", "1080p", "720p", "480p", "360p", "Audio Only (MP3)"]
                }
        except Exception:
            pass

        # Fallback to pytube
        try:
            from pytube import YouTube
            yt = YouTube(url)
            return {
                "url": url,
                "title": yt.title,
                "author": yt.author,
                "duration": yt.length,
                "views": yt.views,
                "thumbnail_url": yt.thumbnail_url,
                "formats": ["Best Quality", "720p", "480p", "360p", "Audio Only (MP3)"]
            }
        except Exception as e:
            raise RuntimeError(f"Could not extract video metadata: {str(e)}")

    def load_thumbnail(self, thumbnail_url: str, size=(160, 90)):
        if not thumbnail_url:
            return None
        try:
            req = urlopen(thumbnail_url, timeout=5)
            data = req.read()
            img = Image.open(BytesIO(data))
            img.thumbnail(size, Image.Resampling.LANCZOS)
            return img
        except Exception:
            return None

    def download_async(self, url: str, output_path: str, format_choice: str, on_progress, on_success, on_error):
        def _worker():
            try:
                self._do_download(url, output_path, format_choice, on_progress)
                on_success()
            except Exception as e:
                on_error(str(e))

        threading.Thread(target=_worker, daemon=True).start()

    def _do_download(self, url: str, output_path: str, format_choice: str, on_progress):
        # yt-dlp download
        try:
            import yt_dlp

            def ytdl_hook(d):
                if d["status"] == "downloading":
                    total = d.get("total_bytes") or d.get("total_bytes_estimate") or 0
                    downloaded = d.get("downloaded_bytes", 0)
                    pct = (downloaded / total * 100) if total > 0 else 0
                    speed = d.get("_speed_str", "")
                    on_progress(pct, f"Downloading: {pct:.1f}% ({speed})")
                elif d["status"] == "finished":
                    on_progress(100.0, "Processing & converting file...")

            outtmpl = os.path.join(output_path, "%(title)s.%(ext)s")

            if format_choice == "Audio Only (MP3)":
                ydl_opts = {
                    "format": "bestaudio/best",
                    "outtmpl": outtmpl,
                    "postprocessors": [{
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "192",
                    }],
                    "progress_hooks": [ytdl_hook],
                    "quiet": True
                }
            else:
                height_map = {"1080p": 1080, "720p": 720, "480p": 480, "360p": 360}
                if format_choice in height_map:
                    h = height_map[format_choice]
                    fmt = f"bestvideo[height<={h}][ext=mp4]+bestaudio[ext=m4a]/best[height<={h}]"
                else:
                    fmt = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best"

                ydl_opts = {
                    "format": fmt,
                    "outtmpl": outtmpl,
                    "progress_hooks": [ytdl_hook],
                    "quiet": True
                }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            return
        except Exception:
            pass

        # Fallback to pytube
        try:
            from pytube import YouTube

            def pytube_progress(stream, chunk, bytes_remaining):
                total = stream.filesize
                downloaded = total - bytes_remaining
                pct = (downloaded / total * 100) if total > 0 else 0
                on_progress(pct, f"Downloading: {pct:.1f}%")

            yt = YouTube(url, on_progress_callback=pytube_progress)

            if format_choice == "Audio Only (MP3)":
                stream = yt.streams.filter(only_audio=True).first()
                out_file = stream.download(output_path=output_path)
                base, _ = os.path.splitext(out_file)
                os.rename(out_file, base + ".mp3")
            else:
                stream = yt.streams.filter(progressive=True, file_extension="mp4").order_by("resolution").desc().first()
                if not stream:
                    stream = yt.streams.get_highest_resolution()
                stream.download(output_path=output_path)
        except Exception as e:
            raise RuntimeError(f"Download error: {str(e)}")
