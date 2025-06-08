""" A class to interact with a target YouTube video """
import yt_dlp


class TargetVideo(object):
    """ A target YouTube video to interact with """
    def __init__(self, video_id: str, title: str):
        self.title: str = title
        self.video_id: str = video_id
        self.video_url: str = f'https://www.youtube.com/watch?v={self.video_id}'

    def download_video(self) -> None:
        """
        Download the video associated with the target video.

        Returns:
            None

        """
        options = {
            'outtmpl': '%(title)s.%(ext)s',  # Save location and file naming
            'format': 'bestvideo+bestaudio/best',  # Best video and audio format
            'merge_output_format': 'mp4',  # Ensure merged-format is mp4
        }

        with yt_dlp.YoutubeDL(options) as video:
            print("Downloading video...")
            video.download([self.video_url])

    def download_captions(self, download: bool = False) -> None:
        """
        Downloads the video captions for a given video URL, specifically in English.
        Prefers manually uploaded captions if available; otherwise, downloads auto-generated captions.
        The video itself is not downloaded within this method.

        Returns:
            None
        """
        # Step 1: Extract video info without downloading
        with yt_dlp.YoutubeDL() as ydl:
            info = ydl.extract_info(self.video_url, download=download)

        # Step 2: Check and download manually uploaded captions
        if 'subtitles' in info and 'en' in info['subtitles']:
            options = {
                'writesubtitles': True,  # Enable manual subtitles download
                'subtitleslangs': ['en'],  # Specify English
                'skip_download': True,  # Do not download video
                'outtmpl': self.title  # Use the title provided in __init__
            }
            with yt_dlp.YoutubeDL(options) as ydl:
                print("Downloading manually uploaded captions...")
                ydl.download([self.video_url])
                print("Captions downloaded!")

        # Step 3: Check and download auto-generated captions if manual ones are unavailable
        elif 'automatic_captions' in info and 'en' in info['automatic_captions']:
            options = {
                'writeautomaticsub': True,  # Enable auto-generated subtitles download
                'subtitleslangs': ['en'],  # Specify English
                'skip_download': True,  # Do not download video
                'outtmpl': self.title  # Use the title provided in __init__
            }
            with yt_dlp.YoutubeDL(options) as ydl:
                print("Downloading auto-generated captions...")
                ydl.download([self.video_url])
                print("Captions downloaded!")

        # Step 4: Handle case where no captions are available
        else:
            print("No English captions available.")
