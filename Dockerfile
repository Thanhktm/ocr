FROM nvidia/cuda:12.1.1-cudnn8-runtime-ubuntu22.04

WORKDIR /app

# Install Python and system dependencies
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/* \
    && ln -s /usr/bin/python3 /usr/bin/python

# Upgrade pip
RUN pip install --upgrade pip

# Install PaddlePaddle GPU (CUDA 12.3 compatible with 12.1)
RUN pip install --no-cache-dir paddlepaddle-gpu -i https://www.paddlepaddle.org.cn/packages/stable/cu123/

# Install other dependencies
RUN pip install --no-cache-dir paddleocr runpod

# Download and cache the PaddleOCR-VL model during build
RUN python -c "from paddleocr import PaddleOCRVL; PaddleOCRVL()"

COPY rp_handler.py .

CMD ["python", "-u", "rp_handler.py"]
