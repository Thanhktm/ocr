import runpod
import base64
import os
import tempfile
from paddleocr import PaddleOCRVL

# Initialize model at cold start (model is baked into image)
pipeline = PaddleOCRVL()


def handler(event):
    """
    RunPod serverless handler for PaddleOCR-VL.

    Input:
        - image_base64: Base64 encoded image string
        - image_url: URL to download image from (alternative to base64)
        - output_format: "markdown", "json", or "text" (default: "markdown")

    Output:
        - result: OCR result in requested format
    """
    input_data = event.get("input", {})

    image_base64 = input_data.get("image_base64")
    image_url = input_data.get("image_url")
    output_format = input_data.get("output_format", "markdown")

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

            output = pipeline.predict(image_path)

            results = []
            for res in output:
                if output_format == "markdown":
                    md_path = os.path.join(tmp_dir, "output")
                    res.save_to_markdown(save_path=md_path)
                    md_file = os.path.join(md_path, "output.md")
                    if os.path.exists(md_file):
                        with open(md_file, "r") as f:
                            results.append(f.read())
                elif output_format == "json":
                    results.append(res.json)
                else:
                    results.append(str(res))

            return {"result": results[0] if len(results) == 1 else results}

    except Exception as e:
        return {"error": str(e)}


runpod.serverless.start({"handler": handler})
