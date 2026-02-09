
# YouTube Video Downloader
```

Python tool to download YouTube videos in highest quality.
```

- **GUI** : `youtube_downloader_ui.py` (with progress bar)
- **CLI** : `youtube_downloader_cli.py` (for automation)
- **Input** : YouTube video URL
- **Output** : `[Video Title].mp4` in project folder
```

---
```
## Installation (Windows + venv)

From project root (`youtube-video-downloader/`) :

```cmd
py -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

---

## Install FFmpeg (Required)

1. Download from: https://github.com/BtbN/FFmpeg-Builds/releases
2. Get `ffmpeg-master-latest-win64-gpl.zip`
3. Extract and copy `ffmpeg.exe` to project root:
   ```
   youtube-video-downloader/
   └── ffmpeg.exe   <-- Place here
   ```

---

## Run GUI Version

```cmd
python youtube_downloader_ui.py
```

Steps:
1. Enter YouTube URL
2. Click "Search Resolution"
3. Select resolution from dropdown
4. Click "Download Video"

---

## Run CLI Version

```cmd
python youtube_downloader_cli.py
```

---

## Requirements

`requirements.txt` contains:
```
pytubefix==0.4.1
```

---

## Notes

- FFmpeg is **required** for 720p+ downloads
- Without FFmpeg: Available quality is only 360p 
- Age-restricted videos handled automatically
- Temporary files cleaned up after download
```