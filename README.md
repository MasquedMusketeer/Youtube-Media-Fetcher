# Youtube Media Fetcher v1.0.1

A simple desktop app to download YouTube videos and playlists as MP4 or MP3.

## Requirements

- Python 3.x (auto-installed via `winget` if missing, when launched via `launch.bat`)
- `yt-dlp` (auto-installed if missing)
- `ffmpeg` (required for MP3 conversion and video merging — the app will prompt to install it via `winget` if missing)

## Usage

```bash
python downloader.py
```

1. Paste a YouTube video or playlist URL
2. Choose a save folder
3. Optionally set an alias for the output filename
4. Select output format (MP4 or MP3)
5. Click **Download**

## Features

- Single video and playlist support
- MP4 (best quality) and MP3 (192kbps) output
- Progress bar for single videos, counter for playlists
- Optional filename alias

---

## License

Youtube Media Fetcher - Copyright (C) 2026 Mendoukusai ByteLabs

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.


---

## Author

Made By Masked Musketeer under the Mendoukusai ByteLabs brand
- GitHub: github.com/MasquedMusketeer
- Contact: Mendoukusai.ByteLabs@outlook.com
