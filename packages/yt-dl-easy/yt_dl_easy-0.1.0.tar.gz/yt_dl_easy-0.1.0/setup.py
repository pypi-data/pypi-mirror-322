from setuptools import setup, find_packages

setup(
    name="yt-dl-easy",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "yt-dlp",
        "tqdm",
    ],
    entry_points={
        "console_scripts": [
            "yt-dl=youtube_downloader:main",
        ],
    },
    author="Pratim Bhosale",
    description="A simple YouTube video downloader",
    long_description="A user-friendly command-line tool to download YouTube videos with progress bar",
    keywords="youtube downloader video download yt-dlp",
    python_requires=">=3.6",
)
