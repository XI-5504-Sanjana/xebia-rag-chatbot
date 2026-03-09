from dotenv import load_dotenv
import os

load_dotenv()

from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

vectorstore = FAISS.load_local(
    "vector_store",
    OpenAIEmbeddings(),
    allow_dangerous_deserialization=True
)

docs = vectorstore.similarity_search("start button", k=5)

for d in docs:
    print(d.metadata)
    print(d.page_content)
    print("------")

