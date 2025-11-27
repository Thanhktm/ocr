import runpod
import base64
from openai import OpenAI

# Connect to local vLLM server
client = OpenAI(base_url="http://127.0.0.1:8000/v1", api_key="not-used")
MODEL_NAME = "PaddlePaddle/PaddleOCR-VL"

# Available task prompts
TASK_PROMPTS = {
    "ocr": "OCR:",
    "table": "Table Recognition:",
    "formula": "Formula Recognition:",
    "chart": "Chart Recognition:",
}


def handler(event):
    """
    RunPod serverless handler for PaddleOCR-VL via vLLM.

    Input:
        - image_base64: Base64 encoded image string
        - image_url: URL of the image
        - task: "ocr", "table", "formula", or "chart" (default: "ocr")

    Output:
        - result: Extracted text/content from the image
    """
    input_data = event.get("input", {})

    image_base64 = input_data.get("image_base64")
    image_url = input_data.get("image_url")
    task = input_data.get("task", "ocr")

    if not image_base64 and not image_url:
        return {"error": "Please provide either 'image_base64' or 'image_url'"}

    task_prompt = TASK_PROMPTS.get(task, TASK_PROMPTS["ocr"])

    try:
        # Build image content
        if image_url:
            image_content = {"type": "image_url", "image_url": {"url": image_url}}
        else:
            image_content = {
                "type": "image_url",
                "image_url": {"url": f"data:image/png;base64,{image_base64}"},
            }

        # Call vLLM API
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "user",
                    "content": [
                        image_content,
                        {"type": "text", "text": task_prompt},
                    ],
                }
            ],
            max_tokens=4096,
        )

        result = response.choices[0].message.content
        return {"result": result}

    except Exception as e:
        return {"error": str(e)}


runpod.serverless.start({"handler": handler})
