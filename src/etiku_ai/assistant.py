
from google import genai
from google.genai import types

from src.etiku_ai.config import GEMINI_MODEL, SYSTEM_INSTRUCTION


RESPONSE_STYLES = {
    "Concise": (
        "Give short, direct answers. Focus on the essential "
        "information and avoid unnecessary explanations."
    ),
    "Balanced": (
        "Give clear, helpful, well-structured answers with "
        "enough detail to explain the topic."
    ),
    "Detailed": (
        "Give comprehensive, well-organized explanations. "
        "Include relevant examples and step-by-step guidance "
        "when appropriate."
    ),
}

CREATIVITY_TEMPERATURES = {
    "Precise": 0.2,
    "Balanced": 0.7,
    "Creative": 1.0,
}


def stream_response(
    messages,
    api_key,
    response_style="Balanced",
    creativity="Balanced",
):
    """Generate Gemini streaming responses using chat settings."""

    if not api_key:
        raise ValueError("Gemini API key is not configured.")

    client = genai.Client(api_key=api_key)

    history = []

    for message in messages:
        role = message.get("role")
        content = message.get("content", "")

        if role not in ("user", "assistant"):
            continue

        if not isinstance(content, str) or not content.strip():
            continue

        history.append(
            types.Content(
                role="model" if role == "assistant" else "user",
                parts=[
                    types.Part.from_text(text=content)
                ],
            )
        )

    if not history:
        raise ValueError("No valid messages were provided.")

    # Select response style
    style_instruction = RESPONSE_STYLES.get(
        response_style,
        RESPONSE_STYLES["Balanced"],
    )

    # Select Gemini temperature
    temperature = CREATIVITY_TEMPERATURES.get(
        creativity,
        CREATIVITY_TEMPERATURES["Balanced"],
    )

    # Preserve ETIKU AI's original identity and instructions
    system_instruction = (
        f"{SYSTEM_INSTRUCTION}\n\n"
        f"RESPONSE STYLE:\n{style_instruction}"
    )

    response = client.models.generate_content_stream(
        model=GEMINI_MODEL,
        contents=history,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=temperature,
        ),
    )

    for chunk in response:
        if chunk.text:
            yield chunk.text
