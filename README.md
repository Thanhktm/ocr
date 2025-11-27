# PaddleOCR-VL RunPod Serverless

A RunPod serverless worker for document OCR using PaddleOCR-VL via vLLM.

## Features

- PaddleOCR-VL vision-language model for high-quality OCR
- vLLM for fast inference
- Supports OCR, table recognition, formula recognition, and chart recognition
- Model pre-loaded in Docker image for fast serverless startup

## Project Structure

```
.
├── rp_handler.py      # RunPod handler (calls vLLM API)
├── start.sh           # Starts vLLM server + handler
├── Dockerfile         # CUDA + vLLM + model baked in
├── test_input.json    # Local testing input
└── .runpod/           # RunPod configuration
```

## Build & Deploy

```bash
# Build image (requires GPU machine or cloud build)
docker build --platform linux/amd64 -t thanhnokasoft/paddleocr-vl:latest .

# Push to Docker Hub
docker push thanhnokasoft/paddleocr-vl:latest
```

## API Usage

### Input

```json
{
  "input": {
    "image_url": "https://example.com/document.png",
    "task": "ocr"
  }
}
```

Or with base64:

```json
{
  "input": {
    "image_base64": "<base64 encoded image>",
    "task": "table"
  }
}
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| image_base64 | string | One of these | Base64 encoded image |
| image_url | string | required | URL to image |
| task | string | No | `ocr`, `table`, `formula`, or `chart` (default: `ocr`) |

### Task Types

- **ocr**: General text extraction
- **table**: Table structure recognition
- **formula**: Mathematical formula recognition
- **chart**: Chart/diagram analysis

### Response

```json
{
  "result": "Extracted text content..."
}
```
