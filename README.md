# PaddleOCR-VL RunPod Serverless

A RunPod serverless worker for document OCR using PaddleOCR-VL. The model is baked into the Docker image to reduce cold start time.

## Features

- PaddleOCR-VL for high-quality document OCR
- Supports 109 languages
- Handles text, tables, formulas, and charts
- Model pre-loaded in Docker image for fast serverless startup

## Project Structure

```
.
├── rp_handler.py      # Main handler function
├── requirements.txt   # Python dependencies
├── Dockerfile         # Container configuration (GPU + model baked in)
├── test_input.json    # Local testing input
└── .runpod/           # RunPod configuration
```

## Build & Deploy

```bash
# Build image (requires GPU or build on RunPod/cloud)
docker build --platform linux/amd64 -t thanhnokasoft/paddleocr-vl:latest .

# Push to Docker Hub
docker push thanhnokasoft/paddleocr-vl:latest
```

## API Usage

### Input

```json
{
  "input": {
    "image_base64": "<base64 encoded image>",
    "output_format": "markdown"
  }
}
```

Or using URL:

```json
{
  "input": {
    "image_url": "https://example.com/document.png",
    "output_format": "markdown"
  }
}
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| image_base64 | string | One of these | Base64 encoded image |
| image_url | string | required | URL to download image |
| output_format | string | No | `markdown`, `json`, or `text` (default: `markdown`) |

### Response

```json
{
  "result": "# Document Title\n\nExtracted text content..."
}
```
