"""
NVIDIA OCR API Client Library

This library provides a client interface for the NVIDIA OCR service that returns
raw markdown text output.
"""

from .client import nvOCR

__version__ = "1.0.0"
__all__ = ["nvOCR"]