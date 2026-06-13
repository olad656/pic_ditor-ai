import os
import json
import re

from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("Missing GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)


def extract_json(text: str):
    """
    Extract JSON safely from Gemini response
    """

    try:
        return json.loads(text)
    except Exception:
        pass

    try:
        match = re.search(r"\{.*\}", text, re.DOTALL)

        if match:
            return json.loads(match.group())
    except Exception:
        pass

    return {
        "task": "clarify",
        "message": "Invalid AI response"
    }


class IntentEngine:

    def parse(self, prompt: str):

        system_prompt = f"""
You are an image editing intent parser.

Return ONLY valid JSON.

Allowed tasks:

- remove_background
- enhance_image
- face_swap
- move_object
- replace_text
- crop_image
- blur_object
- sharpen_image
- resize_image
- cartoon_effect
- colorize_image
- remove_object
- generate_image
- clarify

User request:

{prompt}

Examples:

User:
remove background

Output:
{{"task":"remove_background"}}

User:
make image clearer

Output:
{{"task":"enhance_image"}}

User:
blur the person's face

Output:
{{"task":"blur_object"}}

User:
replace the text on the image

Output:
{{"task":"replace_text"}}

Return ONLY JSON.
"""

        try:

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=system_prompt
            )

            text = response.text.strip()

            print("GEMINI RAW RESPONSE:")
            print(text)

            return extract_json(text)

        except Exception as e:

            print("GEMINI ERROR:", str(e))

            return {
                "task": "clarify",
                "message": f"Gemini error: {str(e)}"
            }