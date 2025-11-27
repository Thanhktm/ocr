import runpod
from openai import OpenAI

# Connect to local vLLM server
client = OpenAI(
    api_key="EMPTY",
    base_url="http://localhost:8000/v1",
    timeout=3600
)

# Task-specific base prompts
TASKS = {
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

    task_prompt = TASKS.get(task, TASKS["ocr"])

    try:
        # Build image URL
        if image_url:
            img_url = image_url
        else:
            img_url = f"data:image/png;base64,{image_base64}"

        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": img_url
                        }
                    },
                    {
                        "type": "text",
                        "text": task_prompt
                    }
                ]
            }
        ]

        response = client.chat.completions.create(
            model="PaddlePaddle/PaddleOCR-VL",
            messages=messages,
            temperature=0.0,
        )

        result = response.choices[0].message.content
        return {"result": result}

    except Exception as e:
        return {"error": str(e)}


runpod.serverless.start({"handler": handler})
