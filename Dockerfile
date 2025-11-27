FROM ccr-2vdh3abv-pub.cnc.bj.baidubce.com/paddlepaddle/paddlex-genai-vllm-server

WORKDIR /app

# Install runpod
RUN pip install --no-cache-dir runpod

COPY rp_handler.py .
COPY start.sh .
RUN chmod +x start.sh

CMD ["./start.sh"]
