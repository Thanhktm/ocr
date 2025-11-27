#!/bin/bash

# Start vLLM server in background (exactly as per documentation)
vllm serve PaddlePaddle/PaddleOCR-VL \
    --trust-remote-code \
    --max-num-batched-tokens 16384 \
    --no-enable-prefix-caching \
    --mm-processor-cache-gb 0 &

# Wait for server to be ready
echo "Waiting for vLLM server to start..."
until curl -s http://localhost:8000/health > /dev/null 2>&1; do
    sleep 2
done
echo "vLLM server is ready"

# Start RunPod handler
python -u rp_handler.py
