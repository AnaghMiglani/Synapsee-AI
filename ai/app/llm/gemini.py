from google import genai
from typing import Optional
from ai.app.services.google_trends.main import POPULAR_MARKETS
from ai.app.core.config import GEMINI_API_KEY
client = genai.Client()

def trend_via_gemini(product_name: str, product_desc: str, price: float,region: str, age: Optional[str] = "All age groups") -> str:
    if not age:
        age = "All age groups"
    SYSTEM_PROMPT=f"""You are a market analyzer tool.
Your task is to generate market input for Google Trends based on structured product and market data.
The output will be sent directly to the google_trends API without any modification.

Inputs Provided:

Product name: {product_name}
Product description (features, positioning, use-case): {product_desc}
Target launch region: {region}
Target age group: {age}
Target price: {price} (take currency as per region)
Popular markets list (regions supported for Google Trends): {POPULAR_MARKETS}

Rules for Generation:

- You MUST return a valid JSON object
- The JSON object MUST contain exactly two keys:
  - "keyword": a single concise Google Trends search query string
  - "geo": the single most appropriate region from the popular markets list
- Do NOT include explanations, comments, markdown, or extra keys
- Do NOT include whitespace outside JSON formatting
- Do NOT combine multiple attributes into a long phrase (e.g. avoid "smart fitness watch for teens in India")
- Select the most representative core search term that users are realistically typing
- Prefer category-level or dominant intent keywords over descriptive phrases
- The keyword must maximize relevance, search volume, and trend signal quality
- Use the popular markets list to select the best matching region only
- Do NOT invent regions outside the provided popular markets list

Output Constraint (STRICT):

- Output MUST be valid JSON
- Output MUST contain ONLY:
  {{
    "keyword": "<string>",
    "geo": "<string>"
  }}
- No surrounding text
- No trailing commas
- No markdown
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=SYSTEM_PROMPT
    )
    print(response)
    return(response.text)
