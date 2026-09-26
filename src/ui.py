import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import ImageTk
from . import config
from .downloader import DownloaderEngine
from .utils import resource_path

class YouTubeDownloaderUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.engine = DownloaderEngine()
        self.download_dir = config.DEFAULT_DOWNLOAD_DIR
        self.thumb_photo = None

        self._setup_window()
        self._create_header()
        self._create_input_bar()
        self._create_video_card()
        self._create_download_options()
        self._create_progress_bar()
        self._create_status_bar()

    def _setup_window(self):
        self.root.title(config.APP_TITLE)
        self.root.geometry(f"{config.WINDOW_WIDTH}x{config.WINDOW_HEIGHT}")
        self.root.minsize(580, 620)
        self.root.configure(bg=config.BG_MAIN)

        icon_path = resource_path(config.ICON_FILE)
        if os.path.exists(icon_path):
            try:
                self.root.iconbitmap(icon_path)
            except Exception:
                pass

    def _create_header(self):
        header = tk.Frame(self.root, bg=config.BG_MAIN)
        header.pack(fill="x", padx=20, pady=(16, 8))

        tk.Label(
            header,
            text="YouTube Media Downloader",
            font=config.TITLE_FONT,
            bg=config.BG_MAIN,
            fg=config.FG_MAIN
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Download YouTube videos in MP4 (1080p, 720p, 480p) or extract MP3 audio",
            font=config.SUBTITLE_FONT,
            bg=config.BG_MAIN,
            fg=config.FG_MUTED
        ).pack(anchor="w")

    def _create_input_bar(self):
        card = tk.Frame(
            self.root,
            bg=config.BG_CARD,
            highlightbackground=config.BORDER_CARD,
            highlightthickness=1
        )
        card.pack(fill="x", padx=20, pady=6)

        inner = tk.Frame(card, bg=config.BG_CARD, padx=10, pady=10)
        inner.pack(fill="x")

        self.url_entry = tk.Entry(
            inner,
            font=config.TEXT_FONT,
            bg=config.BG_INPUT,
            fg=config.FG_MAIN,
            insertbackground=config.FG_MAIN,
            relief="flat",
            bd=0,
            highlightthickness=0
        )
        self.url_entry.pack(side="left", fill="x", expand=True, ipady=6, padx=(0, 6))

        tk.Button(
            inner,
            text="Paste",
            command=self._paste_url,
            font=config.BUTTON_FONT,
            bg=config.BG_INPUT,
            fg=config.FG_MAIN,
            bd=0,
            relief="flat",
            padx=10,
            pady=4,
            cursor="hand2"
        ).pack(side="left", padx=(0, 6))

        self.fetch_btn = tk.Button(
            inner,
            text="Fetch Info",
            command=self._fetch_info,
            font=config.BUTTON_FONT,
            bg=config.ACCENT_SECONDARY,
            fg="#FFFFFF",
            activebackground=config.ACCENT_SECONDARY_HOVER,
            activeforeground="#FFFFFF",
            bd=0,
            relief="flat",
            padx=12,
            pady=4,
            cursor="hand2"
        )
        self.fetch_btn.pack(side="right")

    def _create_video_card(self):
        self.video_card = tk.Frame(
            self.root,
            bg=config.BG_CARD,
            highlightbackground=config.BORDER_CARD,
            highlightthickness=1
        )
        self.video_card.pack(fill="x", padx=20, pady=6)

        inner = tk.Frame(self.video_card, bg=config.BG_CARD, padx=12, pady=12)
        inner.pack(fill="x")

        # Thumbnail Label
        self.thumb_label = tk.Label(
            inner,
            text="No Video Loaded",
            font=config.SUBTITLE_FONT,
            bg=config.BG_INPUT,
            fg=config.FG_MUTED,
            width=20,
            height=5
        )
        self.thumb_label.pack(side="left", padx=(0, 12))

        # Details
        meta_frame = tk.Frame(inner, bg=config.BG_CARD)
        meta_frame.pack(side="left", fill="both", expand=True)

        self.title_label = tk.Label(
            meta_frame,
            text="Paste a YouTube link above and click 'Fetch Info'",
            font=(config.FONT_FAMILY, 11, "bold"),
            bg=config.BG_CARD,
            fg=config.FG_MAIN,
            anchor="w",
            wraplength=340,
            justify="left"
        )
        self.title_label.pack(fill="x", anchor="w")

        self.author_label = tk.Label(
            meta_frame,
            text="",
            font=(config.FONT_FAMILY, 9),
            bg=config.BG_CARD,
            fg=config.FG_MUTED,
            anchor="w"
        )
        self.author_label.pack(fill="x", anchor="w", pady=(4, 0))

        self.stats_label = tk.Label(
            meta_frame,
            text="",
            font=(config.FONT_FAMILY, 9),
            bg=config.BG_CARD,
            fg=config.FG_MUTED,
            anchor="w"
        )
        self.stats_label.pack(fill="x", anchor="w", pady=(2, 0))

    def _create_download_options(self):
        card = tk.Frame(
            self.root,
            bg=config.BG_CARD,
            highlightbackground=config.BORDER_CARD,
            highlightthickness=1
        )
        card.pack(fill="x", padx=20, pady=6)

        inner = tk.Frame(card, bg=config.BG_CARD, padx=12, pady=10)
        inner.pack(fill="x")

        # Format / Quality
        row1 = tk.Frame(inner, bg=config.BG_CARD)
        row1.pack(fill="x", pady=4)

        tk.Label(
            row1,
            text="Quality:",
            font=config.LABEL_FONT,
            bg=config.BG_CARD,
            fg=config.FG_MUTED,
            width=10,
            anchor="w"
        ).pack(side="left")

        self.format_var = tk.StringVar(value="Best Quality")
        self.format_combo = ttk.Combobox(
            row1,
            textvariable=self.format_var,
            values=["Best Quality", "1080p", "720p", "480p", "360p", "Audio Only (MP3)"],
            state="readonly",
            width=22
        )
        self.format_combo.pack(side="left")

        # Destination Folder
        row2 = tk.Frame(inner, bg=config.BG_CARD)
        row2.pack(fill="x", pady=4)

        tk.Label(
            row2,
            text="Save To:",
            font=config.LABEL_FONT,
            bg=config.BG_CARD,
            fg=config.FG_MUTED,
            width=10,
            anchor="w"
        ).pack(side="left")

        self.dest_label = tk.Label(
            row2,
            text=self.download_dir,
            font=(config.FONT_FAMILY, 9),
            bg=config.BG_INPUT,
            fg=config.FG_MAIN,
            anchor="w",
            padx=8,
            pady=4
        )
        self.dest_label.pack(side="left", fill="x", expand=True, padx=(0, 6))

        tk.Button(
            row2,
            text="Browse...",
            command=self._choose_folder,
            font=config.BUTTON_FONT,
            bg=config.BG_INPUT,
            fg=config.FG_MAIN,
            bd=0,
            relief="flat",
            padx=8,
            pady=3,
            cursor="hand2"
        ).pack(side="right")

    def _create_progress_bar(self):
        prog_frame = tk.Frame(self.root, bg=config.BG_MAIN)
        prog_frame.pack(fill="x", padx=20, pady=8)

        self.progress = ttk.Progressbar(prog_frame, orient="horizontal", mode="determinate")
        self.progress.pack(fill="x", ipady=2)

        self.download_btn = tk.Button(
            prog_frame,
            text="⬇ Download Media",
            command=self._start_download,
            font=(config.FONT_FAMILY, 11, "bold"),
            bg=config.ACCENT_YT,
            fg="#FFFFFF",
            activebackground=config.ACCENT_YT_HOVER,
            activeforeground="#FFFFFF",
            bd=0,
            relief="flat",
            padx=16,
            pady=8,
            cursor="hand2"
        )
        self.download_btn.pack(fill="x", pady=(10, 0))

    def _create_status_bar(self):
        status_card = tk.Frame(
            self.root,
            bg=config.BG_CARD,
            highlightbackground=config.BORDER_CARD,
            highlightthickness=1
        )
        status_card.pack(fill="x", padx=20, pady=(2, 14))

        self.status_lbl = tk.Label(
            status_card,
            text="Ready.",
            font=config.STATUS_FONT,
            bg=config.BG_CARD,
            fg=config.FG_MUTED,
            anchor="w",
            padx=12,
            pady=6
        )
        self.status_lbl.pack(fill="x")

    def _paste_url(self):
        try:
            url = self.root.clipboard_get()
            self.url_entry.delete(0, tk.END)
            self.url_entry.insert(0, url.strip())
        except Exception:
            pass

    def _choose_folder(self):
        folder = filedialog.askdirectory(initialdir=self.download_dir)
        if folder:
            self.download_dir = folder
            self.dest_label.config(text=folder)

    def _fetch_info(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning("Empty URL", "Please enter a YouTube video URL.")
            return

        self.fetch_btn.config(state="disabled")
        self.status_lbl.config(text="Fetching video metadata...", fg=config.ACCENT_SECONDARY_HOVER)

        def on_success(meta):
            def _apply():
                self.title_label.config(text=meta["title"])
                self.author_label.config(text=f"Channel: {meta['author']}")

                # Duration formatting
                d = meta["duration"]
                m, s = divmod(d, 60)
                h, m = divmod(m, 60)
                dur_str = f"{h:d}:{m:02d}:{s:02d}" if h > 0 else f"{m:02d}:{s:02d}"
                self.stats_label.config(text=f"Duration: {dur_str} | Views: {meta['views']:,}")

                # Thumbnail loading
                thumb = self.engine.load_thumbnail(meta["thumbnail_url"])
                if thumb:
                    self.thumb_photo = ImageTk.PhotoImage(thumb)
                    self.thumb_label.config(image=self.thumb_photo, text="", width=160, height=90)

                self.format_combo.config(values=meta["formats"])
                self.fetch_btn.config(state="normal")
                self.status_lbl.config(text="Metadata fetched successfully.", fg=config.ACCENT_SUCCESS_HOVER)
            self.root.after(0, _apply)

        def on_error(err_msg):
            def _handle():
                self.fetch_btn.config(state="normal")
                self.status_lbl.config(text="Fetch failed.", fg="#EF4444")
                messagebox.showerror("Error", err_msg)
            self.root.after(0, _handle)

        self.engine.fetch_info_async(url, on_success, on_error)

    def _start_download(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning("Missing URL", "Please provide a YouTube video URL.")
            return

        fmt = self.format_var.get()
        self.download_btn.config(state="disabled")
        self.fetch_btn.config(state="disabled")
        self.progress["value"] = 0

        def on_progress(pct, msg):
            self.root.after(0, lambda: [
                self.progress.configure(value=pct),
                self.status_lbl.configure(text=msg, fg=config.ACCENT_SECONDARY_HOVER)
            ])

        def on_success():
            def _apply():
                self.progress["value"] = 100
                self.download_btn.config(state="normal")
                self.fetch_btn.config(state="normal")
                self.status_lbl.config(text="Download finished successfully!", fg=config.ACCENT_SUCCESS_HOVER)
                messagebox.showinfo("Success", f"Download finished!\nSaved to: {self.download_dir}")
            self.root.after(0, _apply)

        def on_error(err_msg):
            def _handle():
                self.download_btn.config(state="normal")
                self.fetch_btn.config(state="normal")
                self.status_lbl.config(text="Download failed.", fg="#EF4444")
                messagebox.showerror("Download Error", f"Failed to download:\n{err_msg}")
            self.root.after(0, _handle)

        self.engine.download_async(url, self.download_dir, fmt, on_progress, on_success, on_error)
