FROM nvidia/cuda:12.4.0-devel-ubuntu22.04

WORKDIR /app

# Install Python and system dependencies
RUN apt-get update && apt-get install -y \
    python3.11 \
    python3-pip \
    python3.11-venv \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && ln -sf /usr/bin/python3.11 /usr/bin/python \
    && ln -sf /usr/bin/python3.11 /usr/bin/python3

# Upgrade pip
RUN pip install --upgrade pip

# Install vLLM nightly (required for PaddleOCR-VL)
RUN pip install --no-cache-dir -U vllm --pre --extra-index-url https://wheels.vllm.ai/nightly

# Install other dependencies
RUN pip install --no-cache-dir runpod openai

# Download model during build to bake into image
RUN python -c "from huggingface_hub import snapshot_download; snapshot_download('PaddlePaddle/PaddleOCR-VL')"

COPY rp_handler.py .
COPY start.sh .
RUN chmod +x start.sh

CMD ["./start.sh"]
