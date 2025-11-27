# Claude Code Instructions

## Project Overview

This is a RunPod serverless worker for PaddleOCR-VL document OCR. The main handler is in `rp_handler.py`.

## Key Files

- `rp_handler.py` - Main handler, accepts image_base64 or image_url, returns OCR result
- `Dockerfile` - Uses NVIDIA CUDA base image, bakes PaddleOCR-VL model into image
- `requirements.txt` - Dependencies: runpod, paddleocr, paddlepaddle-gpu

## Build & Deploy Commands

```bash
# Build Docker image for RunPod (must use linux/amd64, requires GPU)
docker build --platform linux/amd64 -t thanhnokasoft/paddleocr-vl:latest .

# Push to Docker Hub
docker push thanhnokasoft/paddleocr-vl:latest
```

## Docker Hub

- Username: `thanhnokasoft`
- Repository: `paddleocr-vl`

## API Input Format

```json
{
  "input": {
    "image_url": "https://example.com/image.png",
    "output_format": "markdown"
  }
}
```

Or with base64:

```json
{
  "input": {
    "image_base64": "<base64>",
    "output_format": "json"
  }
}
```

## Testing

Local testing uses `test_input.json` which is automatically loaded by the RunPod SDK.
