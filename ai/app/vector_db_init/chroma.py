from pathlib import Path
from ai.app.embeddings.google_embedd import embeddings
BASE_DIR = Path(__file__).resolve().parents[3]
CHROMA_DB_PATH = BASE_DIR / "local_db" / "chroma-db"

# print(CHROMA_DB_PATH)
from langchain_chroma import Chroma

vector_store = Chroma(
    collection_name="raw_material_WPI",
    embedding_function=embeddings,
    persist_directory=str(CHROMA_DB_PATH),
)
