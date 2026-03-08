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
# import fitz
# import os

# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_community.vectorstores import FAISS
# from langchain_openai import OpenAIEmbeddings
# from langchain_core.documents import Document
# from config import OPENAI_API_KEY

# os.makedirs("extracted_images", exist_ok=True)

# doc = fitz.open("data/manual.pdf")

# documents = []

# splitter = RecursiveCharacterTextSplitter(
#     chunk_size=700,
#     chunk_overlap=150
# )

# for page_number in range(len(doc)):

#     page = doc[page_number]

#     text = page.get_text()

#     chunks = splitter.split_text(text)

#     for chunk in chunks:
#         documents.append(
#             Document(
#                 page_content=chunk,
#                 metadata={
#                     "type": "text",
#                     "page": page_number
#                 }
#             )
#         )

#     image_list = page.get_images(full=True)

#     for img_index, img in enumerate(image_list):

#         xref = img[0]

#         base_image = doc.extract_image(xref)

#         image_bytes = base_image["image"]

#         image_name = f"page{page_number}_{img_index}.png"

#         image_path = f"extracted_images/{image_name}"

#         with open(image_path, "wb") as f:
#             f.write(image_bytes)

#         caption = f"Car manual diagram on page {page_number}"

#         documents.append(
#             Document(
#                 page_content=caption,
#                 metadata={
#                     "type": "image",
#                     "page": page_number,
#                     "image_path": image_path
#                 }
#             )
#         )


# embeddings = OpenAIEmbeddings()

# import shutil

# if os.path.exists("vector_store"):
#     shutil.rmtree("vector_store")

# vectorstore = FAISS.from_documents(documents, embeddings)

# vectorstore.save_local("vector_store")

# print("✅ Multimodal ingestion completed")


# import fitz
# import os
# import io
# from PIL import Image
# from caption_generation import generate_caption
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_community.vectorstores import FAISS
# from langchain_openai import OpenAIEmbeddings
# from langchain_core.documents import Document
# from config import OPENAI_API_KEY

# MIN_WIDTH = 250
# MIN_HEIGHT = 250


# def is_meaningful_image(img_bytes: bytes) -> bool:
#     try:
#         img = Image.open(io.BytesIO(img_bytes))
#         w, h = img.size

#         if w < MIN_WIDTH or h < MIN_HEIGHT:
#             return False

#         if w > h * 15 or h > w * 15:
#             return False

#         return True
#     except:
#         return False


# os.makedirs("extracted_images", exist_ok=True)

# doc = fitz.open("data/manual.pdf")

# documents = []

# splitter = RecursiveCharacterTextSplitter(
#     chunk_size=700,
#     chunk_overlap=150
# )

# for page_number in range(len(doc)):

#     page = doc[page_number]

#     text = page.get_text()

#     chunks = splitter.split_text(text)

#     for chunk in chunks:
#         documents.append(
#             Document(
#                 page_content=chunk,
#                 metadata={
#                     "type": "text",
#                     "page": page_number
#                 }
#             )
#         )

#     image_list = page.get_images(full=True)

#     for img_index, img in enumerate(image_list):

#         xref = img[0]

#         base_image = doc.extract_image(xref)

#         image_bytes = base_image["image"]

#         if not is_meaningful_image(image_bytes):
#             continue

#         image_name = f"page{page_number}_{img_index}.png"

#         image_path = f"extracted_images/{image_name}"

#         with open(image_path, "wb") as f:
#             f.write(image_bytes)

#         caption = generate_caption(image_path)

#         documents.append(
#             Document(
#                 page_content=caption,
#                 metadata={
#                     "type": "image",
#                     "page": page_number,
#                     "image_path": image_path
#                 }
#             )
#         )

# embeddings = OpenAIEmbeddings()

# import shutil

# if os.path.exists("vector_store"):
#     shutil.rmtree("vector_store")

# vectorstore = FAISS.from_documents(documents, embeddings)

# vectorstore.save_local("vector_store")

# print("✅ Multimodal ingestion completed")

# import fitz
# import os
# import io
# import shutil
# from PIL import Image

# from caption_generation import generate_caption
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_community.vectorstores import FAISS
# from langchain_openai import OpenAIEmbeddings
# from langchain_core.documents import Document
# from config import OPENAI_API_KEY


# MIN_WIDTH = 250
# MIN_HEIGHT = 250

# IMAGE_DIR = "extracted_images"


# def is_meaningful_image(img_bytes: bytes) -> bool:
#     try:
#         img = Image.open(io.BytesIO(img_bytes))
#         w, h = img.size

#         if w < MIN_WIDTH or h < MIN_HEIGHT:
#             return False

#         if w > h * 15 or h > w * 15:
#             return False

#         return True

#     except:
#         return False


# os.makedirs(IMAGE_DIR, exist_ok=True)

# doc = fitz.open("data/manual.pdf")

# documents = []

# splitter = RecursiveCharacterTextSplitter(
#     chunk_size=700,
#     chunk_overlap=150
# )


# for page_number in range(len(doc)):

#     page = doc[page_number]

#     text = page.get_text()

#     chunks = splitter.split_text(text)

#     for chunk in chunks:
#         documents.append(
#             Document(
#                 page_content=chunk,
#                 metadata={
#                     "type": "text",
#                     "page": page_number
#                 }
#             )
#         )

#     # -------- NEW IMAGE EXTRACTION --------

#     pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))

#     image_path = os.path.join(
#         IMAGE_DIR,
#         f"page_{page_number:03d}.png"
#     )

#     pix.save(image_path)

#     with open(image_path, "rb") as f:
#         img_bytes = f.read()

#     if is_meaningful_image(img_bytes):

#         caption = generate_caption(image_path)
#         # caption = f"Car manual diagram on page {page_number}"

#         documents.append(
#             Document(
#                 page_content=caption,
#                 metadata={
#                     "type": "image",
#                     "page": page_number,
#                     "image_path": image_path
#                 }
#             )
#         )


# embeddings = OpenAIEmbeddings()

# if os.path.exists("vector_store"):
#     shutil.rmtree("vector_store")

# vectorstore = FAISS.from_documents(documents, embeddings)

# vectorstore.save_local("vector_store")

# print("✅ Multimodal ingestion completed")








import fitz
import os
import io
import shutil
import pytesseract
import cv2
import numpy as np
from PIL import Image
import hashlib
import re

from caption_generation import generate_caption
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from config import OPENAI_API_KEY


# ---------- SET TESSERACT PATH ----------
pytesseract.pytesseract.tesseract_cmd = r"Tesseract-OCR\tesseract.exe"


MIN_WIDTH = 250
MIN_HEIGHT = 250

IMAGE_DIR = "extracted_images"

os.makedirs(IMAGE_DIR, exist_ok=True)


# ---------- IMAGE FILTER ----------
def is_meaningful_image(img_bytes: bytes):
    try:
        img = Image.open(io.BytesIO(img_bytes))
        w, h = img.size

        if w < MIN_WIDTH or h < MIN_HEIGHT:
            return False

        if w > h * 15 or h > w * 15:
            return False

        return True
    except:
        return False


# ---------- OCR FUNCTION (IMPROVED) ----------
def extract_text_from_page(page):

    pix = page.get_pixmap(matrix=fitz.Matrix(3, 3))

    img_bytes = pix.tobytes("png")

    img_array = np.frombuffer(img_bytes, np.uint8)

    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # reduce noise
    gray = cv2.GaussianBlur(gray, (5, 5), 0)

    # adaptive threshold for diagrams
    thresh = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11,
        2
    )

    text = pytesseract.image_to_string(
        thresh,
        config="--oem 3 --psm 6"
    )

    return text


doc = fitz.open("data/manual.pdf")

documents = []

splitter = RecursiveCharacterTextSplitter(
    chunk_size=700,
    chunk_overlap=150
)

seen_images = set()


for page_number in range(len(doc)):

    page = doc[page_number]

    # ---------- TEXT EXTRACTION ----------
    pdf_text = page.get_text()

    ocr_text = extract_text_from_page(page)

    # text = pdf_text + "\n" + ocr_text
    text = pdf_text + "\n" + ocr_text

# clean OCR noise
    text = re.sub(r"[^A-Za-z0-9\s:/()-]", " ", text)
    text = re.sub(r"\s+", " ", text)

    chunks = splitter.split_text(text)

    for chunk in chunks:

        chunk = chunk.strip()

        # remove garbage OCR chunks
        if len(chunk) < 40:
            continue

        if chunk.count(" ") < 3:
            continue

        documents.append(
            Document(
                page_content=chunk,
                metadata={
                    "type": "text",
                    "page": page_number
                }
            )
        )


    # ---------- IMAGE EXTRACTION ----------
    for img_idx, img_info in enumerate(page.get_images(full=True)):

        xref = img_info[0]

        base_image = doc.extract_image(xref)

        if not base_image:
            continue

        image_bytes = base_image["image"]

        if not is_meaningful_image(image_bytes):
            continue

        # remove duplicate images
        img_hash = hashlib.md5(image_bytes).hexdigest()

        if img_hash in seen_images:
            continue

        seen_images.add(img_hash)

        ext = base_image.get("ext", "png")

        filename = f"page_{page_number:03d}_extra_{img_idx+1:02d}.{ext}"

        filepath = os.path.join(IMAGE_DIR, filename)

        with open(filepath, "wb") as f:
            f.write(image_bytes)

        caption = generate_caption(filepath)

        documents.append(
            Document(
                page_content=caption,
                metadata={
                    "type": "image",
                    "page": page_number,
                    "image_path": filepath
                }
            )
        )


# ---------- VECTOR STORE ----------
embeddings = OpenAIEmbeddings()

if os.path.exists("vector_store"):
    shutil.rmtree("vector_store")

vectorstore = FAISS.from_documents(documents, embeddings)

vectorstore.save_local("vector_store")

print("✅ Multimodal ingestion completed")