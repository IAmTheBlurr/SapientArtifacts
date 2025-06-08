""" Module to format caption and transcript text for optimal consumption """
import re
from typing import Optional, List


class TextFormatter(object):
    """
    A class to format caption or transcript text for optimal consumption.
    Provides methods to clean, merge, and structure text for various use cases.
    """

    def __init__(self):
        """Initialize the TextFormatter."""
        pass

    def format_as_paragraphs(self, text: str,
                             sentence_endings: Optional[List[str]] = None) -> str:
        """
        Format text by merging short caption lines into natural paragraphs.

        Args:
            text: Raw text with short lines to be merged
            sentence_endings: List of punctuation marks that indicate sentence end.
                            Defaults to ['.', '!', '?', '"', "'"]

        Returns:
            Text formatted as natural paragraphs
        """
        if sentence_endings is None:
            sentence_endings = ['.', '!', '?', '"', "'"]

        # First clean the text
        text = self.remove_artifacts(text)

        # Split into lines
        lines = text.split('\n')

        # Merge lines into paragraphs based on punctuation
        paragraphs = []
        current_paragraph = []

        for line in lines:
            line = line.strip()
            if not line:
                continue

            current_paragraph.append(line)

            # Check if line ends with sentence-ending punctuation
            if any(line.endswith(ending) for ending in sentence_endings):
                # Join the current paragraph and start a new one
                if current_paragraph:
                    paragraph_text = ' '.join(current_paragraph)
                    paragraphs.append(paragraph_text)
                    current_paragraph = []

        # Remember the last paragraph if it exists
        if current_paragraph:
            paragraph_text = ' '.join(current_paragraph)
            paragraphs.append(paragraph_text)

        # Join paragraphs with double newlines
        formatted_text = '\n\n'.join(paragraphs)

        return formatted_text

    def format_for_llm(self, text: str,
                       max_line_length: Optional[int] = None,
                       preserve_speaker_markers: bool = False) -> str:
        """
        Optimize text specifically for LLM ingestion.

        Args:
            text: Text to optimize for LLM processing
            max_line_length: Maximum characters per line (None for no limit)
            preserve_speaker_markers: Whether to keep speaker labels like "SPEAKER:"

        Returns:
            Text optimized for LLM consumption
        """
        # Clean artifacts first
        text = self.remove_artifacts(text)

        # Remove speaker markers if requested
        if not preserve_speaker_markers:
            # Remove patterns like "SPEAKER:" at the start of lines
            text = re.sub(r'^[A-Z][A-Z]+:\s*', '', text, flags=re.MULTILINE)

        # Format as paragraphs
        text = self.format_as_paragraphs(text)

        # Apply line length limit if specified
        if max_line_length:
            text = self._wrap_text(text, max_line_length)

        return text

    @staticmethod
    def remove_artifacts(text: str) -> str:
        """
        Remove HTML entities and clean whitespace.

        Args:
            text: Text containing artifacts to remove

        Returns:
            Cleaned text
        """
        # Remove HTML entities
        text = text.replace('&nbsp;', ' ')
        text = text.replace('&amp;', '&')
        text = text.replace('&lt;', '<')
        text = text.replace('&gt;', '>')
        text = text.replace('&quot;', '"')
        text = text.replace('&#39;', "'")

        # Normalize line breaks
        text = re.sub(r'\r\n', '\n', text)
        text = re.sub(r'\r', '\n', text)

        # Remove excessive whitespace
        text = re.sub(r' +', ' ', text)  # Multiple spaces to single
        text = re.sub(r'\n{3,}', '\n\n', text)  # Multiple newlines to double

        # Clean up space around newlines
        text = re.sub(r' *\n *', '\n', text)

        # Strip leading and trailing whitespace
        text = text.strip()

        return text

    @staticmethod
    def _wrap_text(text: str, max_length: int) -> str:
        """
        Wrap text to specified line length at word boundaries.

        Args:
            text: Text to wrap
            max_length: Maximum line length

        Returns:
            Text with lines wrapped at word boundaries
        """
        paragraphs = text.split('\n\n')
        wrapped_paragraphs = []

        for paragraph in paragraphs:
            if len(paragraph) <= max_length:
                wrapped_paragraphs.append(paragraph)
                continue

            words = paragraph.split()
            lines = []
            current_line = []
            current_length = 0

            for word in words:
                word_length = len(word)
                if current_length + word_length + len(current_line) <= max_length:
                    current_line.append(word)
                    current_length += word_length
                else:
                    if current_line:
                        lines.append(' '.join(current_line))
                    current_line = [word]
                    current_length = word_length

            if current_line:
                lines.append(' '.join(current_line))

            wrapped_paragraphs.append('\n'.join(lines))

        return '\n\n'.join(wrapped_paragraphs)

    @staticmethod
    def export_formatted_text(text: str, filename: str, format_type: str = 'plain') -> None:
        """
        Export formatted text to file with specified format.

        Args:
            text: Formatted text to export
            filename: Base filename (without extension)
            format_type: Export format ('plain', 'markdown', or 'structured')
        """
        if format_type == 'plain':
            output_filename = f'{filename}_formatted.txt'
            with open(output_filename, 'w', encoding='utf-8') as f:
                f.write(text)

        elif format_type == 'markdown':
            output_filename = f'{filename}_formatted.md'
            with open(output_filename, 'w', encoding='utf-8') as f:
                f.write(f'# Formatted Transcript\n\n')
                f.write(f'*Source: {filename}*\n\n')
                f.write('---\n\n')
                f.write(text)

        elif format_type == 'structured':
            output_filename = f'{filename}_formatted_structured.txt'
            with open(output_filename, 'w', encoding='utf-8') as f:
                f.write(f'DOCUMENT: {filename}\n')
                f.write(f'TYPE: Formatted Transcript\n')
                f.write('=' * 50 + '\n\n')
                f.write(text)
                f.write('\n\n' + '=' * 50 + '\n')
                f.write('END OF DOCUMENT\n')

        else:
            raise ValueError(f"Unsupported format type: {format_type}")
