# YouTube Downloader

1. YouTube Video download
   * Single video or All videos from a playlist
   * Download caption option available
   * Highest .mp4 resolution

2. YouTube Audio download
   * Single video or All videos from a playlist
   * Download audio only track to .mp3 file

# Installation
1. Using `pip`
   ```commandline
   pip install youtube-downloader-cli
   ```

2. Using `uv`
   ```commandline
   uv tool install youtube-downloader-cli
   ```

# CLI Application

## Step 1. Enter YouTube video URL (auto-detect from clipboard)

## Step 2. Choose options

### Available options:

1. Download audio only (mp3)
2. Download video and audio (mp4)
3. Download video with caption (srt)
4. Bulk download audios from playlist
5. Bulk download videos from playlist

## Step 3. Choose a directory to save file(s)

Note: If PyTubeFix failed to connect to YouTube, it may need to be upgraded to the newest version.
Using `pip`: `pip install --upgrade pytubefix`. Or using `uv`: `uv install youtube-downloader-cli --upgrade --reinstall`. 

# Dependencies
1. For CLI Application
   * pyperclip
   * pytubefix
   * questionary
   * rich

2. Of `pytubefix`
   * NodeJS (make sure that NodeJS is available for POTOKEN generation from `pytubefix`)
