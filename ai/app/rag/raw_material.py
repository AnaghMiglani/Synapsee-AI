from pathlib import Path
from langchain_chroma import Chroma
from ai.app.embeddings.google_embedd import embeddings

BASE_DIR = Path(__file__).resolve().parents[3]
CHROMA_DB_PATH = BASE_DIR / "local_db" / "chroma-db"

def get_vector_store(collection_name="raw_material_prices"):
    return Chroma(
        collection_name=collection_name,
        embedding_function=embeddings,
        persist_directory=str(CHROMA_DB_PATH),
    )
vector_store = get_vector_store()


CSV_PATH = (
    BASE_DIR
    / "ai"
    / "app"
    / "rag-sources"
    / "cal_year_index(Calender_Year_Index).csv"
)

from langchain_community.document_loaders import CSVLoader

loader = CSVLoader(
    file_path=str(CSV_PATH),
    encoding="utf-8"
)

documents = loader.load()
print(f"Loaded {len(documents)} rows from CSV")
import re
from langchain_core.documents import Document

def enrich_wpi_row(doc: Document) -> Document:
    text = doc.page_content
    cols = text.split("\t")  # TSV structure assumed

    if len(cols) < 4:
        doc.metadata["skip"] = True
        return doc

    name = cols[0].strip()
    code = cols[1].strip()
    weight = cols[2].strip()

    if name.lower() == "all commodities":
        doc.metadata["skip"] = True
        return doc

    if re.match(r"^[IVX]+\s", name):  # Roman numeral sections
        doc.metadata["skip"] = True
        return doc


    if name.startswith("("):
        level = "category"
    elif re.match(r"^[a-z]\.", name):
        level = "sub_category"
    else:
        level = "item"

    clean_name = re.sub(r"^[a-z]\.\s*|\(.*?\)\.?\s*", "", name).strip()

    year_indices = {}
    for i, col in enumerate(cols):
        if col.startswith("INDEX"):
            year = col.replace("INDEX", "")
            try:
                year_indices[year] = float(cols[i])
            except:
                pass

    doc.metadata.update({
        "commodity": clean_name.lower(),
        "level": level,
        "comm_code": code,
        "weight": float(weight),
        "indices": year_indices
    })

    return doc

documents = [enrich_wpi_row(doc) for doc in documents]
documents = [d for d in documents if not d.metadata.get("skip")]

vector_store.add_documents(documents)

print(f"Indexed {len(documents)} WPI rows into ChromaDB at {CHROMA_DB_PATH}")