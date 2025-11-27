import runpod
import base64
import os
import tempfile
import subprocess

VLLM_SERVER_URL = "http://127.0.0.1:8080/v1"


def handler(event):
    """
    RunPod serverless handler for PaddleOCR-VL.

    Input:
        - image_base64: Base64 encoded image string
        - image_url: URL to download image from (alternative to base64)

    Output:
        - result: OCR result in markdown format
    """
    input_data = event.get("input", {})

    image_base64 = input_data.get("image_base64")
    image_url = input_data.get("image_url")

    if not image_base64 and not image_url:
        return {"error": "Please provide either 'image_base64' or 'image_url'"}

    try:
        with tempfile.TemporaryDirectory() as tmp_dir:
            if image_base64:
                image_data = base64.b64decode(image_base64)
                image_path = os.path.join(tmp_dir, "input_image.png")
                with open(image_path, "wb") as f:
                    f.write(image_data)
            else:
                import urllib.request
                image_path = os.path.join(tmp_dir, "input_image.png")
                urllib.request.urlretrieve(image_url, image_path)

            output_dir = os.path.join(tmp_dir, "output")
            os.makedirs(output_dir, exist_ok=True)

            # Run paddleocr CLI with vLLM backend
            cmd = [
                "paddleocr", "doc_parser",
                "-i", image_path,
                "--vl_rec_backend", "vllm-server",
                "--vl_rec_server_url", VLLM_SERVER_URL,
                "-o", output_dir
            ]

            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode != 0:
                return {"error": f"OCR failed: {result.stderr}"}

            # Find and read output markdown
            md_files = [f for f in os.listdir(output_dir) if f.endswith('.md')]
            if md_files:
                with open(os.path.join(output_dir, md_files[0]), "r") as f:
                    return {"result": f.read()}

            return {"result": result.stdout}

    except Exception as e:
        return {"error": str(e)}


runpod.serverless.start({"handler": handler})
