#!/bin/bash

# Start vLLM server in background
python -m vllm.entrypoints.openai.api_server &

# Wait for server to be ready
echo "Waiting for vLLM server to start..."
while ! curl -s http://127.0.0.1:8080/health > /dev/null 2>&1; do
    sleep 2
done
echo "vLLM server is ready"

# Start RunPod handler
python -u rp_handler.py
