import os
import json
import re
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)


def extract_json(text: str):
    try:
        return json.loads(text)
    except:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except:
                pass

    return {"task": "clarify", "steps": []}


class IntentEngine:

    def parse(self, prompt: str):

        system_prompt = f"""
You are an IMAGE EDITING PIPELINE ENGINE.

Convert user request into a STEP-BY-STEP JSON PIPELINE.

RULES:
- Output ONLY valid JSON
- No explanation
- Always break complex requests into steps
- Max 5 steps per pipeline

AVAILABLE OPERATIONS:

background.remove
background.replace
image.enhance
image.upscale
image.blur
image.sharpen
face.beautify
object.remove
text.add
color.adjust
lighting.adjust
resize
crop.auto
style.cartoon
style.oil_painting
style.anime

USER REQUEST:
{prompt}

OUTPUT FORMAT:

{{
  "task": "pipeline",
  "steps": [
    {{
      "operation": "background.remove"
    }},
    {{
      "operation": "image.enhance"
    }}
  ]
}}
"""

        try:
            model = genai.GenerativeModel("gemini-2.5-flash")
            response = model.generate_content(system_prompt)

            return extract_json(response.text)

        except Exception as e:
            return {"task": "clarify", "steps": []}