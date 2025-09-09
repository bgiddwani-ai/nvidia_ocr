# NVIDIA OCR

A Python client library for NVIDIA OCR services.

## Installation

```bash
pip install -e .
```

## Usage

### Basic Usage

```python
from nvidia_ocr import nvOCR

# Initialize the client
client = nvOCR(api_key="your-api-key", url="http://localhost:8000")

# Upload a file
with open("document.pdf", "rb") as f:
    file_data = {
        "file_name": "document.pdf",
        "content": f.read()
    }
    
uploaded_file = client.files.upload(file_data, purpose="ocr")

# Process the uploaded file
result = client.process_uploaded_file(
    file_id=uploaded_file.id,
    prompt_mode="prompt_layout_all_en",
)

print(result)
```

### Process Base64 Image

```python
import base64

# Read and encode image
with open("image.png", "rb") as f:
    image_data = base64.b64encode(f.read()).decode()

document = {
    "image": image_data,
    "filename": "image.png"
}

result = client.process_image(
    document=document,
    prompt_mode="prompt_layout_all_en"
)

print(result)
```

### Get Results

```python
# Get processing results
results = client.get_results(file_id="your-file-id")
print(results)
```

### Download Processed File

```python
# Download processed file
file_content = client.download_file(
    file_id="your-file-id",
    filename="output.txt"
)

with open("downloaded_output.txt", "wb") as f:
    f.write(file_content)
```

### Delete File

```python
# Clean up - delete file and its results
response = client.delete_file(file_id="your-file-id")
print(response)
```

## API Reference

### nvOCR Class

#### `__init__(api_key: str, url: str = "http://localhost:8000")`

Initialize the NVIDIA OCR client.

**Parameters:**
- `api_key`: Your API key for authentication
- `url`: Base URL of the OCR service (default: "http://localhost:8000")

#### `process_uploaded_file(file_id: str, prompt_mode: str = "prompt_layout_all_en") -> Dict[str, Any]`

Process an uploaded file.

**Parameters:**
- `file_id`: ID of the uploaded file
- `prompt_mode`: Processing mode (default: "prompt_layout_all_en")

#### `process_image(document: Dict[str, Any],  prompt_mode: str = "prompt_layout_all_en") -> Dict[str, Any]`

Process a base64 encoded image directly.

**Parameters:**
- `document`: Dictionary containing image data and filename
- `prompt_mode`: Processing mode

#### `get_results(file_id: str) -> Dict[str, Any]`

Get processing results for a file.

#### `download_file(file_id: str, filename: str) -> bytes`

Download a processed file.

#### `delete_file(file_id: str) -> Dict[str, str]`

Delete a file and its processing results.

### FilesClient Class

#### `upload(file: Dict[str, Any], purpose: str = "ocr") -> UploadedFile`

Upload a file for processing.

**Parameters:**
- `file`: Dictionary with 'file_name' and 'content' keys
- `purpose`: Purpose of the upload (default: "ocr")

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
