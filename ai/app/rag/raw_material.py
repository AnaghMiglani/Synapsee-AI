from pathlib import Path
import pandas as pd

from langchain_chroma import Chroma
from langchain_core.documents import Document
from ai.app.embeddings.hugging_face_local_embedd import embeddings

BASE_DIR = Path(__file__).resolve().parents[3]
CHROMA_DB_PATH = BASE_DIR / "local_db" / "chroma-db"

CSV_PATH = (
    BASE_DIR
    / "ai"
    / "app"
    / "rag-sources"
    / "cal_year_index(Calender_Year_Index).csv"
)

df = pd.read_csv(CSV_PATH)

documents = []

for _, row in df.iterrows():
    name = str(row.get("COMM_NAME", "")).strip()

    if not name:
        continue

    if name.lower() == "all commodities":
        continue

    code = row.get("COMM_CODE", "")
    weight = row.get("COMM_WT", "")

    year_values = []
    for col in df.columns:
        if col.startswith("INDEX") and pd.notna(row[col]):
            year = col.replace("INDEX", "")
            year_values.append(f"{year}: {row[col]}")

    if not year_values:
        continue

    content = (
        f"Commodity {name} (code {code}, weight {weight}). "
        f"Wholesale Price Index values are "
        + ", ".join(year_values)
        + "."
    )

    documents.append(
        Document(
            page_content=content,
            metadata={
                "commodity": name.lower(),
                "comm_code": code,
            }
        )
    )

print(f"Prepared documents: {len(documents)}")

texts = [d.page_content for d in documents]
metadatas = [d.metadata for d in documents]

vectors = embeddings.embed_documents(texts)

print("Texts:", len(texts))
print("Vectors:", len(vectors))
print("Vector size:", len(vectors[0]) if vectors else None)

vector_store = Chroma(
    collection_name="raw_material_prices",
    persist_directory=str(CHROMA_DB_PATH),
)

ids = [f"wpi_{i}" for i in range(len(texts))]

vector_store._collection.upsert(
    ids=ids,
    documents=texts,
    metadatas=metadatas,
    embeddings=vectors,
)

print("WPI data indexed successfully")
