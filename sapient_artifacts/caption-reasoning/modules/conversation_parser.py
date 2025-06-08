""" Module to parse speaker-demarcated conversations from caption text """
import re
from typing import List, Dict, Optional


class ConversationParser:
    """
    A class to parse speaker-demarcated conversations from caption text.
    Extracts speaker names and their corresponding dialogue.
    """

    def __init__(self, speaker_patterns: Optional[List[str]] = None):
        """
        Initialize the ConversationParser with speaker patterns.

        Args:
            speaker_patterns: List of speaker demarcation patterns to look for.
                             If None, will auto-detect patterns like "NAME:"
        """
        self.speaker_patterns = speaker_patterns or []
        self.conversation_segments: List[Dict[str, str]] = []

    def parse_conversation(self, text: str, auto_detect_speakers: bool = True) -> List[Dict[str, str]]:
        """
        Parse the conversation text into a list of speaker-text dictionaries.

        Args:
            text: The cleaned caption text to parse
            auto_detect_speakers: If True and no speaker_patterns provided, auto-detect speaker patterns

        Returns:
            List of dictionaries with 'name' and 'text' keys
        """
        if auto_detect_speakers and not self.speaker_patterns:
            self.speaker_patterns = self._auto_detect_speakers(text)

        if not self.speaker_patterns:
            # No speakers detected, return entire text as a single segment
            return [{'name': 'Unknown', 'text': self._clean_text(text)}]

        # Create regex pattern to match any speaker
        speaker_regex = '|'.join(re.escape(pattern) for pattern in self.speaker_patterns)
        pattern = f'({speaker_regex})'

        # Split text by speaker patterns
        segments = re.split(pattern, text)

        # Process segments into conversation list
        self.conversation_segments = []
        current_speaker = None

        for i, segment in enumerate(segments):
            segment = segment.strip()
            if not segment:
                continue

            # Check if this segment is a speaker marker
            if segment in self.speaker_patterns:
                current_speaker = segment.rstrip(':')
            else:
                # This is dialogue text
                if current_speaker:
                    cleaned_text = self._clean_text(segment)
                    if cleaned_text:  # Only add if there's actual content
                        self.conversation_segments.append({
                            'name': current_speaker,
                            'text': cleaned_text
                        })

        return self.conversation_segments

    @staticmethod
    def _auto_detect_speakers(text: str) -> List[str]:
        """
        Auto-detect speaker patterns in the format "NAME:" where NAME is all caps.

        Args:
            text: The text to analyze for speaker patterns

        Returns:
            List of detected speaker patterns
        """
        # Pattern to match "ALLCAPS:" at the beginning of a line or after punctuation
        pattern = r'(?:^|\s|[.!?])\s*([A-Z][A-Z]+):'

        matches = re.findall(pattern, text)
        unique_speakers = list(set(matches))

        # Convert to full patterns with colons
        speaker_patterns = [f"{speaker}:" for speaker in unique_speakers]

        return speaker_patterns

    @staticmethod
    def _clean_text(text: str) -> str:
        """
        Clean the text by removing line breaks, HTML entities, and extra whitespace.

        Args:
            text: The text to clean

        Returns:
            Cleaned text with single spaces between words
        """
        # Remove HTML non-breaking space entities
        text = text.replace('&nbsp;', ' ')

        # Replace various line break patterns with spaces
        text = re.sub(r'[\r\n]+', ' ', text)

        # Replace multiple spaces with single space
        text = re.sub(r'\s+', ' ', text)

        # Remove leading/trailing whitespace
        text = text.strip()

        return text

    def merge_consecutive_speakers(self) -> List[Dict[str, str]]:
        """
        Merge consecutive segments from the same speaker.

        Returns:
            List of merged conversation segments
        """
        if not self.conversation_segments:
            return []

        merged = []
        current_segment = self.conversation_segments[0].copy()

        for segment in self.conversation_segments[1:]:
            if segment['name'] == current_segment['name']:
                # Same speaker, merge text
                current_segment['text'] += ' ' + segment['text']
            else:
                # Different speaker, save current and start new
                merged.append(current_segment)
                current_segment = segment.copy()

        # Remember the last segment
        merged.append(current_segment)

        return merged

    def export_to_file(self, filename: str, data_format: str = 'text') -> None:
        """
        Export the conversation to a file.

        Args:
            filename: The output filename
            data_format: Export data format ('text', 'json', or 'markdown')
        """
        if not self.conversation_segments:
            raise ValueError("No conversation segments to export")

        if data_format == 'text':
            with open(filename, 'w', encoding='utf-8') as f:
                for segment in self.conversation_segments:
                    f.write(f"{segment['name']}: {segment['text']}\n\n")

        elif data_format == 'json':
            import json
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.conversation_segments, f, indent=2, ensure_ascii=False)

        elif data_format == 'markdown':
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("# Conversation Transcript\n\n")
                for segment in self.conversation_segments:
                    f.write(f"**{segment['name']}**: {segment['text']}\n\n")
        else:
            raise ValueError(f"Unsupported data format: {data_format}")
