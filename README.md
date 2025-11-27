# RunPod Serverless Hello World

A simple RunPod serverless worker that returns a greeting.

## Project Structure

```
.
├── rp_handler.py      # Main handler function
├── requirements.txt   # Python dependencies
├── Dockerfile         # Container configuration
├── test_input.json    # Local testing input
└── .runpod/           # RunPod configuration
```

## Local Development

```bash
pip install -r requirements.txt
python rp_handler.py
```

## Build & Deploy

```bash
# Build image
docker build --platform linux/amd64 -t thanhnokasoft/hello-runpod:latest .

# Push to Docker Hub
docker push thanhnokasoft/hello-runpod:latest
```

## Usage

Send a request with:

```json
{
  "input": {
    "name": "World"
  }
}
```

Response:

```
Hello, World!
```
