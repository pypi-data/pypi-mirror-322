from setuptools import setup, find_packages

setup(
    name="yt-dl-easy",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "yt-dlp",
        "tqdm",
    ],
    entry_points={
        "console_scripts": [
            "yt-dl=youtube_downloader_pkg:main",
        ],
    },
    author="Pratim Bhosale",
    description="A simple YouTube video downloader",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    keywords="youtube downloader video download yt-dlp",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Multimedia :: Video",
    ],
)
