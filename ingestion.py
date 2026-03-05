import fitz
import os
import requests
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.docstore.document import Document
from config import *

os.makedirs("extracted_images", exist_ok=True)

# -------- Get Microsoft Graph Access Token --------
def get_access_token():
    url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"

    data = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "scope": "https://graph.microsoft.com/.default"
    }

    response = requests.post(url, data=data)
    return response.json()["access_token"]


access_token = get_access_token()

headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/octet-stream"
}

doc = fitz.open("data/car_manual.pdf")

page_wise_text = {}
image_metadata = []

# -------- Process Top 10 Pages --------
for page_number in range(10):
    page = doc[page_number]
    text = page.get_text()
    page_wise_text[page_number] = text

    image_list = page.get_images(full=True)

    for img_index, img in enumerate(image_list):
        xref = img[0]
        base_image = doc.extract_image(xref)
        image_bytes = base_image["image"]

        image_name = f"page{page_number}_{img_index}.png"
        local_path = f"extracted_images/{image_name}"

        with open(local_path, "wb") as f:
            f.write(image_bytes)

        # -------- Upload to SharePoint --------
        upload_url = f"https://graph.microsoft.com/v1.0/sites/{SHAREPOINT_SITE_ID}/drives/{SHAREPOINT_DRIVE_ID}/root:/CarManualImages/{image_name}:/content"

        with open(local_path, "rb") as f:
            upload_response = requests.put(upload_url, headers=headers, data=f)

        image_url = upload_response.json()["webUrl"]

        image_metadata.append({
            "page": page_number,
            "image_url": image_url
        })

# -------- Chunk Text --------
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

documents = []

for page_number, text in page_wise_text.items():
    chunks = splitter.split_text(text)

    image_url = None
    for img in image_metadata:
        if img["page"] == page_number:
            image_url = img["image_url"]

    for chunk in chunks:
        documents.append(
            Document(
                page_content=chunk,
                metadata={
                    "page": page_number,
                    "image_url": image_url
                }
            )
        )

# -------- Create Vector DB --------
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(documents, embeddings)
vectorstore.save_local("vector_store")

print("✅ Ingestion Completed with SharePoint Upload!")