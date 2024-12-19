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
            'merge_output_format': 'mp4',  # Ensure merged format is mp4
        }

        with yt_dlp.YoutubeDL(options) as video:
            print("Downloading video...")
            video.download([self.video_url])

    def download_captions(self) -> None:
        """
        Downloads the video captions for a given video URL, specifically in English, and checks if the
        captions are available in the desired language before downloading. The video itself is not
        downloaded within this method.

        Returns:
            None
        """
        captions_opts = {
            'writesubtitles': True,  # Enable subtitles download
            'subtitleslangs': ['en'],  # Specify English subtitles
            'skip_download': True,  # Do not download video here
        }

        with yt_dlp.YoutubeDL(captions_opts) as video:
            print("Downloading captions...")
            info = video.extract_info(self.video_url, download=False)

            if 'subtitles' in info and 'en' in info['subtitles']:
                video.download([self.video_url])
                print("Captions downloaded!")
            else:
                print("No English captions available.")
