from google import genai
from ai.app.services.google_trends.main import get_google_trends_serpapi, POPULAR_MARKETS
from ai.app.core.config import GEMINI_API_KEY
from typing import Optional, List, Dict, Any
import json
from langchain_chroma import Chroma
from ai.app.embeddings.hugging_face_local_embedd import embeddings
from pathlib import Path
from ai.app.services.scraping_amazon.scrape_amazon import scrape_via_render

BASE_DIR = Path(__file__).resolve().parents[3]
CHROMA_DB_PATH = BASE_DIR / "local_db" / "chroma-db"

vector_store = Chroma(
    collection_name="raw_material_prices",
    persist_directory=str(CHROMA_DB_PATH),
    embedding_function=embeddings
)

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
- The JSON object MUST contain exactly three keys:
  - "keyword": a single concise Google Trends search query string
  - "geo": the single most appropriate region from the popular markets list
  - "raw_material": an array of short strings
- "raw_material" rules:
  - Derive materials/components directly from the product description
  - Maximum length of the list is 5
  - Each entry must be 1-3 words only
  - Use generic, searchable terms (no sentences)
- Do NOT include explanations, comments, markdown, or extra keys
- Do NOT include whitespace outside JSON formatting
- Do NOT combine multiple attributes into a long phrase
- Select the most representative core search term that users are realistically typing
- Prefer category-level or dominant intent keywords over descriptive phrases
- The keyword must maximize relevance, search volume, and trend signal quality
- Use the popular markets list only to select the best matching region (used in geo)
- Do NOT invent regions outside the provided popular markets list

Output Constraint (STRICT):

- Output MUST be valid JSON
- Output MUST contain ONLY:
  {{
    "keyword": "<string>",
    "geo": "<string>",
    "raw_material": ["<string>", "<string>"]
  }}
- No surrounding text
- No trailing commas
- No markdown
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=SYSTEM_PROMPT
    )
    print("Response from STEP 1 ")
    print(response)
    return(response.text)

def data_retrieve(
    product_name: str,
    product_desc: str,
    price: float,
    region: str,
    age: Optional[str] = "All age groups"
) -> Dict[Any, Any]:

    raw_output = trend_via_gemini(
        product_name=product_name,
        product_desc=product_desc,
        price=price,
        region=region,
        age=age
    )

    data = json.loads(raw_output.strip())

    keyword = data["keyword"]
    geo = data["geo"]
    raw_materials = data["raw_material"]

    rag_results = []

    try:
        for material in raw_materials:
            query = f"{material} price {geo}"
            docs = vector_store.similarity_search(query, k=2)

            for doc in docs:
                rag_results.append(doc.page_content)
    except:
        rag_results = ["No results found from rag, estimate the price"]

    final_data={}
    final_data["rag_results"] = rag_results

    try:
        trends=get_google_trends_serpapi(keyword=keyword, geo=geo)
    except:
        trends = ["No results found from google trends, estimate the demand"]
    if not trends:
        trends = ["No results found from google trends, estimate the demand"]
    final_data["trends"] = trends

    try:
        scraped_data=scrape_via_render(keyword=keyword)
    except:
        scraped_data="No results found from scraping, estimate the price and competition"
    final_data["scraped_data"] = scraped_data

    print("Response from STEP 2")
    print(final_data)
    return final_data

results = data_retrieve(
    product_name="Electric Sweater",
    product_desc="Battery powered sweater with embedded heating elements",
    price=3499,
    region="India"
)
