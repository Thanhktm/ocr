# Claude Code Instructions

## Project Overview

This is a RunPod serverless worker project. The main handler is in `rp_handler.py`.

## Build & Deploy Commands

```bash
# Build Docker image for RunPod (must use linux/amd64)
docker build --platform linux/amd64 -t thanhnokasoft/hello-runpod:latest .

# Push to Docker Hub
docker push thanhnokasoft/hello-runpod:latest
```

## Docker Hub

- Username: `thanhnokasoft`
- Repository: `hello-runpod`

## Testing

Local testing uses `test_input.json` which is automatically loaded by the RunPod SDK.
