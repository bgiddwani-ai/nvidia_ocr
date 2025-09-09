# NVIDIA OCR Client Library

A Python client library for the NVIDIA OCR API that provides simplified access to optical character recognition services. The library supports both PDF documents and images, returning processed content as raw markdown text.

## Features

- 🔄 **Unified Interface**: Same workflow for PDFs and images
- 📄 **Multiple Formats**: Support for PDF, JPEG, PNG, and TIFF files
- 🚀 **Simple API**: Easy-to-use methods for quick processing
- 📤 **Flexible Upload**: Multiple upload options (direct path, manual, base64)
- 🔍 **Health Monitoring**: Built-in service health checks
- 📝 **Markdown Output**: Clean, structured text output


## Installation

```bash
pip install -e .
```
## Quick Start

```python
from nvidia_ocr import nvOCR

# Initialize the client
client = nvOCR(api_key="your-api-key", url="http://localhost:8001")

# Process a file directly (recommended)
result = client.process_file_direct("path/to/your/document.pdf")
print(result)
```

## Supported File Formats

| Format | Extensions | Description |
|--------|------------|-------------|
| PDF | `.pdf` | Portable Document Format |
| JPEG | `.jpg`, `.jpeg` | JPEG images |
| PNG | `.png` | Portable Network Graphics |
| TIFF | `.tiff`, `.tif` | Tagged Image File Format |

## Usage Examples

### Method 1: Direct File Processing (Recommended)

This is the simplest method for one-time file processing:

```python
from nvidia_ocr import nvOCR

# Initialize client
client = nvOCR(api_key="your-api-key", url="http://localhost:8001")

# Process PDF
pdf_result = client.process_file_direct("./documents/invoice.pdf")
print("PDF Content:")
print(pdf_result)

# Process Image
image_result = client.process_file_direct("./images/receipt.jpg")
print("Image Content:")
print(image_result)

# Custom prompt mode
result = client.process_file_direct(
    "./documents/form.png",
    prompt_mode="prompt_layout_all_en"
)
```

### Method 2: Upload from File Path

Useful when you want to keep the uploaded file for multiple processing operations:

```python
# Upload a file
uploaded_file = client.files.upload_from_path("./documents/contract.pdf")
print(f"Uploaded: {uploaded_file.filename} (ID: {uploaded_file.id})")

# Process the uploaded file
result = client.process_uploaded_file(uploaded_file.id)
print(result)

# Process again with different settings
result2 = client.process_uploaded_file(
    uploaded_file.id,
    prompt_mode="custom_mode"
)
```

### Method 3: Manual File Upload

For more control over the upload process:

```python
# Read file manually
with open("./documents/report.pdf", "rb") as f:
    file_data = {
        "file_name": "report.pdf",
        "content": f.read()
    }

# Upload
uploaded_file = client.files.upload(file_data, purpose="ocr")

# Process
result = client.process_uploaded_file(uploaded_file.id)
print(result)
```

### Method 4: Base64 Image Processing

For processing base64 encoded images directly:

```python
import base64

# Read and encode image
with open("./images/document.jpg", "rb") as f:
    image_data = base64.b64encode(f.read()).decode()

# Create document structure
document = {
    "type": "image_url",
    "image_url": {
        "url": f"data:image/jpeg;base64,{image_data}"
    }
}

# Process
result = client.process_image(document)
print(result)
```

## Advanced Usage

### Batch Processing

Process multiple files efficiently:

```python
import os
from pathlib import Path

def process_directory(directory_path, client):
    """Process all supported files in a directory."""
    supported_formats = client.get_supported_formats()
    results = {}
    
    for file_path in Path(directory_path).iterdir():
        if file_path.suffix.lower() in supported_formats:
            try:
                print(f"Processing: {file_path.name}")
                result = client.process_file_direct(file_path)
                results[file_path.name] = result
            except Exception as e:
                print(f"Error processing {file_path.name}: {e}")
                results[file_path.name] = None
    
    return results

# Usage
client = nvOCR(api_key="your-api-key", url="http://localhost:8001")
batch_results = process_directory("./documents", client)
```

### Error Handling

Implement robust error handling:

```python
def safe_process_file(client, file_path):
    """Safely process a file with comprehensive error handling."""
    try:
        # Check if file exists
        if not Path(file_path).exists():
            return {"error": "File not found", "content": None}
        
        # Check file format
        supported = client.get_supported_formats()
        if Path(file_path).suffix.lower() not in supported:
            return {"error": "Unsupported file format", "content": None}
        
        # Process file
        result = client.process_file_direct(file_path)
        return {"error": None, "content": result}
        
    except Exception as e:
        return {"error": str(e), "content": None}

# Usage
result = safe_process_file(client, "./documents/test.pdf")
if result["error"]:
    print(f"Processing failed: {result['error']}")
else:
    print("Success:", result["content"])
```

### Health Check and Service Monitoring

Monitor the OCR service status:

```python
def check_service_health(client):
    """Check if the OCR service is healthy."""
    try:
        health = client.health_check()
        print("Service Status:", health)
        return True
    except Exception as e:
        print(f"Service health check failed: {e}")
        return False

# Usage
if check_service_health(client):
    # Proceed with OCR operations
    result = client.process_file_direct("./document.pdf")
else:
    print("Service is not available")
```

## Configuration

### Client Configuration

```python
# Basic configuration
client = nvOCR(
    api_key="your-api-key",
    url="http://localhost:8001"
)

# Production configuration
client = nvOCR(
    api_key="prod-api-key",
    url="https://your-ocr-service.com"
)
```

### Prompt Modes

Different processing modes available:

| Mode | Description |
|------|-------------|
| `prompt_layout_all_en` | Default English layout processing |
| `custom_mode` | Custom processing mode |

```python
# Using different prompt modes
result = client.process_file_direct(
    "document.pdf",
    prompt_mode="prompt_layout_all_en"
)
```

## API Reference

### nvOCR Class

#### `__init__(api_key: str, url: str = "http://localhost:8000")`
Initialize the NVIDIA OCR client.

#### `process_file_direct(file_path: Union[str, Path], prompt_mode: str = "prompt_layout_all_en") -> str`
Upload and process a file in one step.

#### `process_uploaded_file(file_id: str, prompt_mode: str = "prompt_layout_all_en") -> str`
Process a previously uploaded file.

#### `process_image(document: Dict[str, Any], prompt_mode: str = "prompt_layout_all_en") -> str`
Process a base64 encoded image.

#### `health_check() -> Dict[str, Any]`
Check the health status of the OCR service.

#### `get_supported_formats() -> list`
Get list of supported file formats.

### FilesClient Class

#### `upload(file: Dict[str, Any], purpose: str = "ocr") -> UploadedFile`
Upload a file for OCR processing.

#### `upload_from_path(file_path: Union[str, Path], purpose: str = "ocr") -> UploadedFile`
Upload a file directly from a file path.

## Error Handling

The library raises the following exceptions:

- `FileNotFoundError`: When specified file doesn't exist
- `ValueError`: When file data is invalid
- `Exception`: For API errors (upload/processing failures)

Always wrap OCR operations in try-catch blocks:

```python
try:
    result = client.process_file_direct("document.pdf")
    print(result)
except FileNotFoundError:
    print("File not found")
except ValueError as e:
    print(f"Invalid file data: {e}")
except Exception as e:
    print(f"OCR processing failed: {e}")
```

## Performance Tips

1. **Use direct processing** for one-time operations
2. **Upload once, process multiple times** for files needing different processing modes
3. **Batch process** similar files together
4. **Monitor service health** before processing large batches
5. **Handle errors gracefully** to avoid interrupting batch operations

## Troubleshooting

### Common Issues

**Connection Error**
```python
# Check if service is running
try:
    health = client.health_check()
    print("Service is running")
except:
    print("Cannot connect to OCR service")
```

**File Format Issues**
```python
# Check supported formats
supported = client.get_supported_formats()
file_ext = Path("your_file.xyz").suffix.lower()
if file_ext not in supported:
    print(f"Unsupported format: {file_ext}")
    print(f"Supported: {supported}")
```

**Large File Processing**
- For large files, consider breaking them into smaller chunks
- Monitor memory usage during processing
- Implement timeout handling for long-running operations

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:
- Check the troubleshooting section
- Review the API reference
- Submit an issue on the project repository
