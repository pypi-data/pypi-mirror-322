import argparse
import os
import yt_dlp
from tqdm import tqdm

class VideoDownloader:
    def __init__(self, output_dir="downloads"):
        """Initialize the downloader with an output directory."""
        self.output_dir = output_dir
        # Create the output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

    def download_video(self, url, resolution="best"):
        """
        Download a video from YouTube.
        
        Args:
            url (str): The YouTube video URL
            resolution (str): Desired resolution ("best" or "720p", "480p", etc.)
        """
        try:
            # Configure yt-dlp options
            ydl_opts = {
                'format': f'bestvideo[height<={resolution[:-1]}]+bestaudio/best' if resolution != "best" else 'best',
                'outtmpl': os.path.join(self.output_dir, '%(title)s.%(ext)s'),
                'progress_hooks': [self._progress_hook],
                'quiet': True,
                'no_warnings': True,
            }

            # Create progress bar
            self.progress_bar = None
            
            print("\nFetching video information...")
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Get video information
                info = ydl.extract_info(url, download=False)
                print(f"Title: {info['title']}")
                print(f"Duration: {info['duration'] // 60}:{info['duration'] % 60:02d} minutes")
                if 'view_count' in info:
                    print(f"Views: {info['view_count']:,}")
                
                print(f"\nDownloading video to: {self.output_dir}")
                # Download the video
                ydl.download([url])
            
            print(f"\nSuccessfully downloaded: {info['title']}")
            
        except Exception as e:
            print(f"Error downloading video: {str(e)}")
        finally:
            if self.progress_bar:
                self.progress_bar.close()

    def _progress_hook(self, d):
        if d['status'] == 'downloading':
            if not self.progress_bar:
                total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
                self.progress_bar = tqdm(
                    total=100,
                    desc="Downloading",
                    unit="%",
                    bar_format='{desc}: {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]'
                )
            
            if d.get('total_bytes') or d.get('total_bytes_estimate', 0):
                downloaded = d.get('downloaded_bytes', 0)
                total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
                if total > 0:
                    percentage = (downloaded / total) * 100
                    self.progress_bar.update(percentage - self.progress_bar.n)

def main():
    parser = argparse.ArgumentParser(description='Download YouTube videos')
    parser.add_argument('url', help='YouTube video URL')
    parser.add_argument('--resolution', default='best',
                      help='Desired resolution (e.g., "720p", "1080p", or "best")')
    parser.add_argument('--output-dir', default='downloads',
                      help='Output directory for downloaded videos')
    
    args = parser.parse_args()
    
    downloader = VideoDownloader(output_dir=args.output_dir)
    downloader.download_video(args.url, args.resolution)

if __name__ == '__main__':
    main()