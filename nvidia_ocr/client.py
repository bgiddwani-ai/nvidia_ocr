"""
NVIDIA OCR Client Library

This module provides a simplified client interface that returns raw markdown text.
"""

import os
import requests
import base64
from typing import Dict, Any
from dataclasses import dataclass

@dataclass
class UploadedFile:
    """Represents an uploaded file in the OCR service."""
    id: str
    purpose: str
    filename: str
    bytes: int
    created_at: int
    status: str

class FilesClient:
    """Client for file upload operations."""
    
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.api_key = api_key
        self.session = requests.Session()
        
    def upload(self, file: Dict[str, Any], purpose: str = "ocr") -> UploadedFile:
        """
        Upload a file for OCR processing.
        
        Args:
            file: Dictionary containing 'file_name' and 'content' keys
            purpose: Purpose of the upload (default: "ocr")
            
        Returns:
            UploadedFile: Information about the uploaded file
            
        Raises:
            ValueError: If file dictionary is invalid
            Exception: If upload fails
        """
        if "file_name" not in file or "content" not in file:
            raise ValueError("File must contain 'file_name' and 'content' keys")
        
        files = {
            "file": (file["file_name"], file["content"])
        }
        
        data = {
            "purpose": purpose
        }
        
        response = self.session.post(
            f"{self.base_url}/v1/files",
            files=files,
            data=data
        )
        
        if response.status_code != 200:
            raise Exception(f"Upload failed: {response.text}")
        
        result = response.json()
        return UploadedFile(**result)

class nvOCR:
    """
    Main client class for NVIDIA OCR API.
    
    This class provides methods to upload files and process images, returning
    raw markdown text as output.
    """
    
    def __init__(self, api_key: str, url: str = "http://localhost:8000"):
        """
        Initialize the NVIDIA OCR client.
        
        Args:
            api_key: API key for authentication (currently not used but required for interface)
            url: Base URL of the OCR service
        """
        self.api_key = api_key
        self.url = url.rstrip('/')
        self.session = requests.Session()
        
        # Initialize clients
        self.files = FilesClient(self.url, api_key)
    
    def process_uploaded_file(
        self, 
        file_id: str, 
        prompt_mode: str = "prompt_layout_all_en"
    ) -> str:
        """
        Process an uploaded file and return markdown text.
        
        Args:
            file_id: ID of the uploaded file
            prompt_mode: OCR processing mode
            
        Returns:
            str: Raw markdown text content
            
        Raises:
            Exception: If processing fails
        """
        response = self.session.post(
            f"{self.url}/v1/ocr/process_file/{file_id}",
            params={
                "prompt_mode": prompt_mode
            }
        )
        
        if response.status_code != 200:
            raise Exception(f"Processing failed: {response.text}")
        
        # Return just the markdown text
        return response.text
    
    def process_image(
        self,
        document: Dict[str, Any],
        prompt_mode: str = "prompt_layout_all_en"
    ) -> str:
        """
        Process a base64 encoded image and return markdown text.
        
        Args:
            document: Dictionary containing image data with 'type' and 'image_url' keys
            prompt_mode: OCR processing mode
            
        Returns:
            str: Raw markdown text content
            
        Raises:
            Exception: If processing fails
        """
        request_data = {
            "document": document,
            "prompt_mode": prompt_mode
        }
        
        response = self.session.post(
            f"{self.url}/v1/ocr/process_image",
            json=request_data
        )
        
        if response.status_code != 200:
            raise Exception(f"Processing failed: {response.text}")
        
        # Return just the markdown text
        return response.text
    
    def health_check(self) -> Dict[str, Any]:
        """
        Check the health status of the OCR service.
        
        Returns:
            Dict containing service health information
            
        Raises:
            Exception: If health check fails
        """
        response = self.session.get(f"{self.url}/health")
        
        if response.status_code != 200:
            raise Exception(f"Health check failed: {response.text}")
        
        return response.json()