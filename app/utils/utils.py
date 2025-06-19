def extract_gemini_response_text(response_data: dict) -> str:
    """
    Extracts the text from a Gemini API response JSON.

    Args:
        response_data (dict): The response JSON from Gemini API.

    Returns:
        str: The extracted text, or an empty string if not found.
    """
    candidates = response_data.get("candidates", [{}])
    if not candidates:
        return ""
    content = candidates[0].get("content", {})
    parts = content.get("parts", [{}])
    if not parts:
        return ""
    return parts[0].get("text", "")