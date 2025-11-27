# Claude Code Instructions

## Project Overview

RunPod serverless worker for PaddleOCR-VL using vLLM as inference backend.

## Architecture

1. `start.sh` starts vLLM server with PaddleOCR-VL model
2. Waits for server to be ready on port 8000
3. Starts `rp_handler.py` which accepts RunPod requests
4. Handler calls vLLM via OpenAI-compatible API

## Key Files

- `rp_handler.py` - RunPod handler, uses OpenAI client to call local vLLM
- `start.sh` - Startup script, launches vLLM server + handler
- `Dockerfile` - CUDA 12.4 + vLLM nightly + model baked in

## Build & Deploy

```bash
# Build (requires GPU or cloud build service)
docker build --platform linux/amd64 -t thanhnokasoft/paddleocr-vl:latest .

# Push
docker push thanhnokasoft/paddleocr-vl:latest
```

## Docker Hub

- Username: `thanhnokasoft`
- Repository: `paddleocr-vl`

## API Input

```json
{
  "input": {
    "image_url": "https://example.com/image.png",
    "task": "ocr"
  }
}
```

Tasks: `ocr`, `table`, `formula`, `chart`

## vLLM Server Config

```bash
vllm serve PaddlePaddle/PaddleOCR-VL \
    --trust-remote-code \
    --max-num-batched-tokens 16384 \
    --no-enable-prefix-caching \
    --mm-processor-cache-gb 0
```
