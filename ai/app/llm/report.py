from google import genai
from datetime import datetime
from ai.app.core.config import GEMINI_API_KEY
from typing import Dict, Any
from ai.app.llm.gemini import data_retrieve

client = genai.Client(api_key=GEMINI_API_KEY)

def generate_report_llm(product_name: str, product_desc: str, price: float, region: str, age: str) -> str:

    data = data_retrieve(
        product_name=product_name,
        product_desc=product_desc,
        price=price,
        region=region,
        age=age
    )

    now = datetime.now()
    date_str = f"{now.day} {now.strftime('%B')} {now.year}"

    prompt = f"""
You are a market research analyst.

Generate a structured business report using the provided data.

Inputs:

Product Name: {product_name}
Product Description: {product_desc}
Target Price: {price}
Region: {region}
Target Age Group: {age}
Current Date: {date_str}

RAG Raw Material Insights:
{data.get("rag_results")}

Google Trends Data:
{data.get("trends")}

Market Scraping Data:
{data.get("scraped_data")}

Instructions:

- Analyze all inputs deeply
- Infer demand cycles from trends data
- Identify best months to SELL
- Estimate production time assuming small scale manufacturing
- Suggest when to START production so product hits peak demand
- Use reasoning, not fixed rules

Output Format (STRICT JSON):

{{
  "Item": "",
  "Age Group": "",
  "Raw Material Insights": "",
  "Monthly Insights (Google Trends)": "",
  "Production Time": "",
  "Suggested Start Month": ""
}}

Rules:

- No markdown
- No explanation
- Only valid JSON
- Keep outputs concise but insightful
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text

report = generate_report_llm(
    product_name="Electric Sweater",
    product_desc="Battery powered sweater with embedded heating elements",
    price=3499,
    region="India",
    age="18-45"
)

print(report)