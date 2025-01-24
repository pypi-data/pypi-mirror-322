# YouTube Video Downloader (yt-dl-easy)

A simple, user-friendly command-line tool to download YouTube videos with progress tracking. Built on top of yt-dlp with a simplified interface.

## Features

- 🚀 Simple command-line interface
- 📊 Real-time download progress bar
- 🎥 Support for various video resolutions
- 📁 Custom output directory
- 📝 Video information display (title, duration, views)
- ⚡ Fast downloads using yt-dlp backend

## Installation

You can install the package directly from PyPI:

```bash
pip install yt-dl-easy
```

Or install from source:

```bash
git clone https://github.com/yourusername/youtube_downloader.git
cd youtube_downloader
pip install .
```

## Usage

After installation, you can use the `yt-dl` command from anywhere in your terminal:

### Basic Usage

Download a video with best quality:
```bash
yt-dl "https://www.youtube.com/watch?v=VIDEO_ID"
```

### Advanced Options

1. Download with specific resolution:
```bash
yt-dl "https://www.youtube.com/watch?v=VIDEO_ID" --resolution 720p
```

2. Specify output directory:
```bash
yt-dl "https://www.youtube.com/watch?v=VIDEO_ID" --output-dir ~/Downloads/videos
```

### Available Options

- `--resolution`: Video resolution (e.g., "720p", "1080p", or "best")
- `--output-dir`: Directory to save downloaded videos (default: "downloads")

## Requirements

- Python 3.6 or higher
- yt-dlp
- tqdm (for progress bar)

## Development

Want to contribute? Great! Here's how you can help:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- Progress bar by [tqdm](https://github.com/tqdm/tqdm)

## Support

If you encounter any issues or have suggestions, please [open an issue](https://github.com/yourusername/youtube_downloader/issues) on GitHub.
