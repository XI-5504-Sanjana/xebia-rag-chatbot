# import fitz # read pdf
# import os 
# import requests # api calls 
# from langchain.text_splitter import RecursiveCharacterTextSplitter #splits large text into chunks
# from langchain.vectorstores import FAISS # vector database
# from langchain_openai import OpenAIEmbeddings #convert text -> vectors
# from langchain.docstore.document import Document 
# from config import * #in cronfig storing credentials and ids

# os.makedirs("extracted_images", exist_ok=True) #created folder for extracted images

# # -------- Get Microsoft Graph Access Token --------
# def get_access_token(): #authenticates your program with Microsoft Azure / SharePoint.
#     url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token" #Microsoft’s OAuth authentication endpoint.
 
#     data = { #Send credentials 
#         "grant_type": "client_credentials",
#         "client_id": CLIENT_ID,
#         "client_secret": CLIENT_SECRET,
#         "scope": "https://graph.microsoft.com/.default"
#     }

#     response = requests.post(url, data=data) #Request token
#     return response.json()["access_token"] #Extract token


# access_token = get_access_token()

# headers = { #These headers are required for uploading files via Graph API.
#     "Authorization": f"Bearer {access_token}",
#     "Content-Type": "application/octet-stream"
# }

# doc = fitz.open("data/car_manual.pdf") #open the car manual pdf

# page_wise_text = {} #stors text of each page
# image_metadata = [] # stores uploaded imag info 

# # Process Top 10 Pages extract text 
# for page_number in range(10):
#     page = doc[page_number] 
#     text = page.get_text()
#     page_wise_text[page_number] = text

#     image_list = page.get_images(full=True)

#     for img_index, img in enumerate(image_list):
#         xref = img[0]
#         base_image = doc.extract_image(xref)
#         image_bytes = base_image["image"]

#         image_name = f"page{page_number}_{img_index}.png" #Save Image Locally
#         local_path = f"extracted_images/{image_name}"

#         with open(local_path, "wb") as f:
#             f.write(image_bytes)

#         # -------- Upload to SharePoint --------
#         upload_url = f"https://graph.microsoft.com/v1.0/sites/{SHAREPOINT_SITE_ID}/drives/{SHAREPOINT_DRIVE_ID}/root:/CarManualImages/{image_name}:/content"

#         with open(local_path, "rb") as f:
#             upload_response = requests.put(upload_url, headers=headers, data=f)

#         image_url = upload_response.json()["webUrl"]
#         #Store Image Metadata

#         image_metadata.append({
#             "page": page_number,
#             "image_url": image_url
#         })

# # -------- Chunk Text --------
# splitter = RecursiveCharacterTextSplitter(
#     chunk_size=500,
#     chunk_overlap=100
# )

# documents = []

# for page_number, text in page_wise_text.items():
#     chunks = splitter.split_text(text)

#     image_url = None
#     for img in image_metadata:
#         if img["page"] == page_number:
#             image_url = img["image_url"]

#     for chunk in chunks:
#         documents.append(
#             Document(
#                 page_content=chunk,
#                 metadata={
#                     "page": page_number,
#                     "image_url": image_url
#                 }
#             )
#         )

# # -------- Create Vector DB --------
# embeddings = OpenAIEmbeddings() #Create Embeddings
# vectorstore = FAISS.from_documents(documents, embeddings) #Create FAISS Vector Database
# vectorstore.save_local("vector_store")

# print("✅ Ingestion Completed with SharePoint Upload!")

#attaches only 1 image per page
# import fitz
# import os
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.vectorstores import FAISS
# from langchain_openai import OpenAIEmbeddings
# from langchain.docstore.document import Document

# os.makedirs("extracted_images", exist_ok=True)

# doc = fitz.open("data/manual.pdf")

# page_wise_text = {}
# image_metadata = []

# # -------- Extract Text + Images --------
# for page_number in range(len(doc)):

#     page = doc[page_number]
#     text = page.get_text()

#     page_wise_text[page_number] = text

#     image_list = page.get_images(full=True)

#     for img_index, img in enumerate(image_list):

#         xref = img[0]
#         base_image = doc.extract_image(xref)
#         image_bytes = base_image["image"]

#         image_name = f"page{page_number}_{img_index}.png"
#         local_path = f"extracted_images/{image_name}"

#         with open(local_path, "wb") as f:
#             f.write(image_bytes)

#         image_metadata.append({
#             "page": page_number,
#             "image_path": local_path
#         })


# # -------- Chunk Text --------

# splitter = RecursiveCharacterTextSplitter(
#     chunk_size=700,
#     chunk_overlap=150
# )

# documents = []

# for page_number, text in page_wise_text.items():

#     chunks = splitter.split_text(text)

#     image_path = None
#     for img in image_metadata:
#         if img["page"] == page_number:
#             image_path = img["image_path"]

#     for chunk in chunks:

#         documents.append(
#             Document(
#                 page_content=chunk,
#                 metadata={
#                     "page": page_number,
#                     "image_path": image_path
#                 }
#             )
#         )


# # -------- Create Vector DB --------

# embeddings = OpenAIEmbeddings()

# vectorstore = FAISS.from_documents(documents, embeddings)

# vectorstore.save_local("vector_store")

# print("✅ Ingestion completed with local images")

#ingestion.py (Multimodal Version)
import fitz
import os

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from config import OPENAI_API_KEY

os.makedirs("extracted_images", exist_ok=True)

doc = fitz.open("data/manual.pdf")

documents = []

splitter = RecursiveCharacterTextSplitter(
    chunk_size=700,
    chunk_overlap=150
)

for page_number in range(len(doc)):

    page = doc[page_number]

    text = page.get_text()

    chunks = splitter.split_text(text)

    for chunk in chunks:
        documents.append(
            Document(
                page_content=chunk,
                metadata={
                    "type": "text",
                    "page": page_number
                }
            )
        )

    image_list = page.get_images(full=True)

    for img_index, img in enumerate(image_list):

        xref = img[0]

        base_image = doc.extract_image(xref)

        image_bytes = base_image["image"]

        image_name = f"page{page_number}_{img_index}.png"

        image_path = f"extracted_images/{image_name}"

        with open(image_path, "wb") as f:
            f.write(image_bytes)

        caption = f"Car manual diagram on page {page_number}"

        documents.append(
            Document(
                page_content=caption,
                metadata={
                    "type": "image",
                    "page": page_number,
                    "image_path": image_path
                }
            )
        )


embeddings = OpenAIEmbeddings()

import shutil

if os.path.exists("vector_store"):
    shutil.rmtree("vector_store")

vectorstore = FAISS.from_documents(documents, embeddings)

vectorstore.save_local("vector_store")

print("✅ Multimodal ingestion completed")
