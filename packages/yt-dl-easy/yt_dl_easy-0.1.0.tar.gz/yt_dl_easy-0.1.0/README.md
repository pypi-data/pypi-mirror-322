# YouTube Video Downloader

A simple command-line tool to download YouTube videos with progress tracking.

## Installation

```bash
pip install .
```

## Usage

After installation, you can use the command `yt-dl` from anywhere in your terminal:

```bash
# Download video with best quality
yt-dl "https://www.youtube.com/watch?v=VIDEO_ID"

# Download with specific resolution
yt-dl "https://www.youtube.com/watch?v=VIDEO_ID" --resolution 720p

# Specify output directory
yt-dl "https://www.youtube.com/watch?v=VIDEO_ID" --output-dir ~/Downloads/videos
```

## Features

- Simple command-line interface
- Progress bar with download status
- Resolution selection
- Custom output directory
- Video information display (title, duration, views)
