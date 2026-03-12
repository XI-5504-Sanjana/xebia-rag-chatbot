# from dotenv import load_dotenv
# import os

# load_dotenv()

# from langchain_community.vectorstores import FAISS
# from langchain_openai import OpenAIEmbeddings

# vectorstore = FAISS.load_local(
#     "vector_store",
#     OpenAIEmbeddings(),
#     allow_dangerous_deserialization=True
# )

# docs = vectorstore.similarity_search("start button", k=5)

# for d in docs:
#     print(d.metadata)
#     print(d.page_content)
#     print("------")


import os
import json
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

# 1) Load environment (expects OPENAI_API_KEY in .env or environment)
load_dotenv()

# 2) Load FAISS vector store
embeddings = OpenAIEmbeddings()  # optionally: OpenAIEmbeddings(model="text-embedding-3-large")
vectorstore = FAISS.load_local(
    "vector_store",
    embeddings,
    allow_dangerous_deserialization=True  # required if index saved with older LC versions
)

# 3) Run a sample query and take top 3 chunks
query = "start button"
k = 3
docs = vectorstore.similarity_search(query, k=k)

# 4) Build a compact JSON payload
results = []
for d in docs:
    meta = d.metadata or {}
    results.append({
        "page": meta.get("page"),
        "chunk_id": meta.get("chunk_id"),
        "source": meta.get("source"),
        "visual_count": len(meta.get("visuals", [])) if isinstance(meta.get("visuals"), list) else 0,
        "visuals": [
            {
                "path": v.get("path"),
                "caption_preview": (v.get("caption") or "")[:80]
            }
            for v in meta.get("visuals", [])[:3]  # keep just a few for preview
        ],
        "text_full": d.page_content,                         # full chunk text
        "text_preview": d.page_content[:200] + ("..." if len(d.page_content) > 200 else ""),  # trim for readability
        "query": query
    })

# 5) Save to a JSON file
out_path = "sample_chunks.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

# 6) Also print to console
print(f"\nSaved {len(results)} chunks to {out_path}\n")
for i, r in enumerate(results, 1):
    print(f"[{i}] page={r['page']} chunk_id={r['chunk_id']} source={r['source']}")
    print(f"    visuals={r['visual_count']}  text_preview={r['text_preview']}")
    print("------")