import os

# Window Configuration
APP_TITLE = "YouTube Media Downloader"
WINDOW_WIDTH = 680
WINDOW_HEIGHT = 680
ICON_FILE = "yt.ico"

# Typography
FONT_FAMILY = "Segoe UI"
TITLE_FONT = (FONT_FAMILY, 15, "bold")
SUBTITLE_FONT = (FONT_FAMILY, 9)
LABEL_FONT = (FONT_FAMILY, 10, "bold")
TEXT_FONT = (FONT_FAMILY, 11)
BUTTON_FONT = (FONT_FAMILY, 10, "bold")
STATUS_FONT = (FONT_FAMILY, 10, "italic")

# Theme Palette (Modern YouTube Dark)
BG_MAIN = "#0F0F0F"
BG_CARD = "#1F1F1F"
BORDER_CARD = "#2E2E2E"
BG_INPUT = "#272727"
FG_MAIN = "#F1F1F1"
FG_MUTED = "#AAAAAA"

# Accents
ACCENT_YT = "#FF0000"           # YouTube Red
ACCENT_YT_HOVER = "#CC0000"
ACCENT_SECONDARY = "#3EA6FF"    # YouTube Blue
ACCENT_SECONDARY_HOVER = "#65B8FF"
ACCENT_SUCCESS = "#2BA640"      # Green
ACCENT_SUCCESS_HOVER = "#3CD055"

# Default download folder
DEFAULT_DOWNLOAD_DIR = os.path.expanduser("~/Downloads")
