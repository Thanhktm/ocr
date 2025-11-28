#!/bin/bash

# Set environment variables for vLLM
export VLLM_ATTENTION_BACKEND=FLASHINFER

# Start vLLM server (exactly as per documentation)
vllm serve PaddlePaddle/PaddleOCR-VL \
    --trust-remote-code \
    --max-num-batched-tokens 16384 \
    --no-enable-prefix-caching \
    --mm-processor-cache-gb 0 \
    --gpu-memory-utilization 0.9 &

VLLM_PID=$!

# Wait for server to be ready
echo "Waiting for vLLM server to start..."
for i in {1..120}; do
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        echo "vLLM server is ready"
        break
    fi

    # Check if vLLM process is still running
    if ! kill -0 $VLLM_PID 2>/dev/null; then
        echo "vLLM server failed to start"
        exit 1
    fi

    sleep 2
done

# Start RunPod handler
python -u rp_handler.py
