from typing import List, Optional
import re

class TextChunker:
    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
        separator: str = " "
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separator = separator

    def split_text(self, text: str) -> List[str]:
        """Split text into chunks with overlap."""
        # Clean and normalize text
        text = self._normalize_text(text)
        
        # If text is shorter than chunk_size, return as single chunk
        if len(text) <= self.chunk_size:
            return [text]

        chunks = []
        start = 0
        text_length = len(text)

        while start < text_length:
            # Get chunk of text
            end = start + self.chunk_size
            
            # If this is not the end of text, try to find a good break point
            if end < text_length:
                # Look for the last separator in the chunk
                last_separator = text.rfind(self.separator, start, end)
                if last_separator != -1:
                    end = last_separator

            # Add the chunk
            chunks.append(text[start:end].strip())
            
            # Move start position, accounting for overlap
            start = end - self.chunk_overlap

        return chunks

    def _normalize_text(self, text: str) -> str:
        """Normalize text by cleaning whitespace and other issues."""
        # Replace multiple whitespace with single space
        text = re.sub(r'\s+', ' ', text)
        # Remove leading/trailing whitespace
        return text.strip() 