import runpod


def handler(event):
    """
    RunPod serverless handler function.
    """
    input_data = event.get("input", {})
    name = input_data.get("name", "World")

    return f"Hello, {name}!"


runpod.serverless.start({"handler": handler})
