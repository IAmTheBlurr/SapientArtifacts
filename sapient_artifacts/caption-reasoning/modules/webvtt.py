""" Module to handle WebVTT files, providing methods to validate and extract caption text. """
import os
import re

from typing import Optional, List


class WebVTT(object):
    """
    A class to handle WebVTT files, providing methods to validate and extract caption text.
    Designed to be extensible for future enhancements.
    """

    CAPTION_SLICE_INDICATOR_PATTERN = r'<c>'
    TIMESTAMP_SHORT_PATTERN = r'<\d{2}:\d{2}:\d{2}\.\d{3}>'
    TIMESTAMP_LONG_PATTERN = r'\d{2}:\d{2}:\d{2}\.\d{3}\s+-->\s+\d{2}:\d{2}:\d{2}\.\d{3}'

    def __init__(self, file_path, strip_headers: bool = False):
        """
        Initialize the WebVTT object with a file path to a .vtt file.

        Args:
            file_path (str): Full path to the .vtt file.
            strip_headers (bool): If True, removes the WebVTT header from the content.

        Raises:
            FileNotFoundError: If the specified file does not exist or is not a file.
        """
        self.content: Optional[str] = None
        self.headers_stripped: bool = False

        self.load_file(file_path)

        if strip_headers:
            self.strip_header()

    def get_only_captions_text(self, strip_headers: bool = False) -> str:
        """
        Extracts only the caption text from the WebVTT file, excluding any other content.

        Args:
            strip_headers (bool): If True, removes the WebVTT header before extracting captions.

        Returns:
            str: The caption text extracted from the WebVTT file.
        """
        if strip_headers and not self.headers_stripped:
            self.strip_header()

        captions_only: List[str] = []
        lines = self.content.split('\n')

        for line in lines:
            empty_line = len(line) < 5
            short_timestamp_exists = re.search(self.TIMESTAMP_SHORT_PATTERN, line)
            long_timestamp_exists = re.search(self.TIMESTAMP_LONG_PATTERN, line)
            caption_slice_exists = re.search(self.CAPTION_SLICE_INDICATOR_PATTERN, line)
            line_present = line not in captions_only

            if (not empty_line and line_present
                    and not short_timestamp_exists
                    and not long_timestamp_exists
                    and not caption_slice_exists):
                captions_only.append(line)

        return "\n".join(captions_only)

    def load_file(self, file_path: str) -> None:
        """
        Load the content of the WebVTT file.

        Args:
            file_path (str): Full path to the .vtt file.

        Returns:
            None

        """
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"No such file: '{file_path}'")

        with open(file_path, encoding='utf-8') as webvtt_file:
            self.content = webvtt_file.read()

    def strip_header(self):
        """
        Iterate over the first few lines of the vtt file and remove the noted details

        Notes:
            Lines to remove if they contain the following
            - WEBVTT
            - Kind
            - Language

        Returns:
            str: The content without the WebVTT header

        """
        # Split the content into lines and remove the header lines
        lines = self.content.split('\n')
        header_lines = ['WEBVTT', 'Kind', 'Language']
        stripped_content = [line for line in lines if not any(header in line for header in header_lines)]

        # Join the remaining lines back into a single string
        self.content = '\n'.join(stripped_content)
        self.headers_stripped = True
