from langchain_chroma import Chroma
from ai.app.embeddings.hugging_face_local_embedd import embeddings
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[3]
CHROMA_DB_PATH = BASE_DIR / "local_db" / "chroma-db"

vector_store = Chroma(
    collection_name="raw_material_prices",
    persist_directory=str(CHROMA_DB_PATH),
)

results = vector_store.similarity_search("brinjal wholesale price index", k=3)

for r in results:
    print(r.page_content)
