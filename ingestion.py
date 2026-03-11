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








# import fitz
# import os
# import io
# import shutil
# import pytesseract
# import cv2
# import numpy as np
# from PIL import Image
# import hashlib
# import re

# from caption_generation import generate_caption
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_community.vectorstores import FAISS
# from langchain_openai import OpenAIEmbeddings
# from langchain_core.documents import Document
# from config import OPENAI_API_KEY


# # ---------- SET TESSERACT PATH ----------
# pytesseract.pytesseract.tesseract_cmd = r"Tesseract-OCR\tesseract.exe"


# MIN_WIDTH = 250
# MIN_HEIGHT = 250

# IMAGE_DIR = "extracted_images"

# os.makedirs(IMAGE_DIR, exist_ok=True)


# # ---------- IMAGE FILTER ----------
# def is_meaningful_image(img_bytes: bytes):
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


# # ---------- OCR FUNCTION (IMPROVED) ----------
# def extract_text_from_page(page):

#     pix = page.get_pixmap(matrix=fitz.Matrix(3, 3))

#     img_bytes = pix.tobytes("png")

#     img_array = np.frombuffer(img_bytes, np.uint8)

#     img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#     # reduce noise
#     gray = cv2.GaussianBlur(gray, (5, 5), 0)

#     # adaptive threshold for diagrams
#     thresh = cv2.adaptiveThreshold(
#         gray,
#         255,
#         cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
#         cv2.THRESH_BINARY,
#         11,
#         2
#     )

#     text = pytesseract.image_to_string(
#         thresh,
#         config="--oem 3 --psm 6"
#     )

#     return text


# doc = fitz.open("data/manual.pdf")

# documents = []

# splitter = RecursiveCharacterTextSplitter(
#     chunk_size=700,
#     chunk_overlap=150
# )

# seen_images = set()


# for page_number in range(len(doc)):

#     page = doc[page_number]

#     # ---------- TEXT EXTRACTION ----------
#     pdf_text = page.get_text()

#     ocr_text = extract_text_from_page(page)

#     # text = pdf_text + "\n" + ocr_text
#     text = pdf_text + "\n" + ocr_text

# # clean OCR noise
#     text = re.sub(r"[^A-Za-z0-9\s:/()-]", " ", text)
#     text = re.sub(r"\s+", " ", text)

#     chunks = splitter.split_text(text)

#     for chunk in chunks:

#         chunk = chunk.strip()

#         # remove garbage OCR chunks
#         if len(chunk) < 40:
#             continue

#         if chunk.count(" ") < 3:
#             continue

#         documents.append(
#             Document(
#                 page_content=chunk,
#                 metadata={
#                     "type": "text",
#                     "page": page_number
#                 }
#             )
#         )


#     # ---------- IMAGE EXTRACTION ----------
#     for img_idx, img_info in enumerate(page.get_images(full=True)):

#         xref = img_info[0]

#         base_image = doc.extract_image(xref)

#         if not base_image:
#             continue

#         image_bytes = base_image["image"]

#         if not is_meaningful_image(image_bytes):
#             continue

#         # remove duplicate images
#         img_hash = hashlib.md5(image_bytes).hexdigest()

#         if img_hash in seen_images:
#             continue

#         seen_images.add(img_hash)

#         ext = base_image.get("ext", "png")

#         filename = f"page_{page_number:03d}_extra_{img_idx+1:02d}.{ext}"

#         filepath = os.path.join(IMAGE_DIR, filename)

#         with open(filepath, "wb") as f:
#             f.write(image_bytes)

#         caption = generate_caption(filepath)

#         documents.append(
#             Document(
#                 page_content=caption,
#                 metadata={
#                     "type": "image",
#                     "page": page_number,
#                     "image_path": filepath
#                 }
#             )
#         )


# # ---------- VECTOR STORE ----------
# embeddings = OpenAIEmbeddings()

# if os.path.exists("vector_store"):
#     shutil.rmtree("vector_store")

# vectorstore = FAISS.from_documents(documents, embeddings)

# vectorstore.save_local("vector_store")

# print("✅ Multimodal ingestion completed")



# # using pymupdf
# import fitz
# import os
# import io
# import shutil
# import pytesseract
# import cv2
# import numpy as np
# from PIL import Image
# import hashlib
# import re
# import json

# from caption_generation import generate_caption
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_community.vectorstores import FAISS
# from langchain_openai import OpenAIEmbeddings
# from langchain_core.documents import Document


# pytesseract.pytesseract.tesseract_cmd = r"Tesseract-OCR\tesseract.exe"

# IMAGE_DIR = "extracted_images"
# os.makedirs(IMAGE_DIR, exist_ok=True)

# MIN_WIDTH = 250
# MIN_HEIGHT = 250


# def is_meaningful_image(img_bytes):

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


# def extract_text_from_page(page):

#     pix = page.get_pixmap(matrix=fitz.Matrix(3,3))

#     img_bytes = pix.tobytes("png")

#     img_array = np.frombuffer(img_bytes, np.uint8)

#     img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#     gray = cv2.GaussianBlur(gray,(5,5),0)

#     thresh = cv2.adaptiveThreshold(
#         gray,
#         255,
#         cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
#         cv2.THRESH_BINARY,
#         11,
#         2
#     )

#     text = pytesseract.image_to_string(thresh)

#     return text


# doc = fitz.open("data/manual.pdf")

# documents = []
# debug_chunks = []

# splitter = RecursiveCharacterTextSplitter(
#     chunk_size=700,
#     chunk_overlap=150
# )

# seen_images = set()


# for page_number in range(len(doc)):

#     page = doc[page_number]

#     pdf_text = page.get_text()

#     ocr_text = extract_text_from_page(page)

#     text = pdf_text + "\n" + ocr_text

#     text = re.sub(r"[^A-Za-z0-9\s:/()-]", " ", text)
#     text = re.sub(r"\s+", " ", text)

#     page_images = []

#     # ---------- EMBEDDED IMAGE EXTRACTION ----------
#     for img_idx, img_info in enumerate(page.get_images(full=True)):

#         xref = img_info[0]

#         base_image = doc.extract_image(xref)

#         if not base_image:
#             continue

#         image_bytes = base_image["image"]

#         if not is_meaningful_image(image_bytes):
#             continue

#         img_hash = hashlib.md5(image_bytes).hexdigest()

#         if img_hash in seen_images:
#             continue

#         seen_images.add(img_hash)

#         ext = base_image.get("ext","png")

#         filename = f"page_{page_number:03d}_img_{img_idx+1}.{ext}"

#         filepath = os.path.join(IMAGE_DIR, filename)

#         with open(filepath,"wb") as f:
#             f.write(image_bytes)

#         caption = generate_caption(filepath)

#         if caption is None:
#             continue

#         page_images.append({
#             "path": filepath,
#             "caption": caption
#         })


#     # ---------- PAGE IMAGE FALLBACK ----------
#     if len(page_images) == 0:

#         pix = page.get_pixmap(matrix=fitz.Matrix(2,2))

#         filename = f"page_{page_number:03d}_full.png"

#         filepath = os.path.join(IMAGE_DIR, filename)

#         pix.save(filepath)

#         caption = generate_caption(filepath)

#         if caption is not None:

#             page_images.append({
#                 "path": filepath,
#                 "caption": caption
#             })


#     # ---------- CHUNKING ----------
#     chunks = splitter.split_text(text)

#     for chunk_id, chunk in enumerate(chunks):

#         chunk = chunk.strip()

#         if len(chunk.split()) < 2:
#             continue

#         metadata = {
#             "page": page_number,
#             "chunk_id": chunk_id,
#             "images": page_images
#         }

#         documents.append(
#             Document(
#                 page_content=chunk,
#                 metadata=metadata
#             )
#         )

#         debug_chunks.append({
#             "page": page_number,
#             "chunk_id": chunk_id,
#             "text": chunk,
#             "images": page_images
#         })


# embeddings = OpenAIEmbeddings()

# if os.path.exists("vector_store"):
#     shutil.rmtree("vector_store")

# vectorstore = FAISS.from_documents(documents, embeddings)

# vectorstore.save_local("vector_store")


# with open("chunks_debug.json","w",encoding="utf-8") as f:
#     json.dump(debug_chunks,f,indent=2,ensure_ascii=False)


# print("Multimodal ingestion completed")


import os
import shutil
import hashlib
import re
import json

from unstructured.partition.pdf import partition_pdf
from caption_generation import generate_caption
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document

print("\n========== STARTING INGESTION ==========\n")

FIGURE_DIR = "figures"
EXTRACTED_FIGURE_DIR = "extracted_figures"

os.makedirs(FIGURE_DIR, exist_ok=True)
os.makedirs(EXTRACTED_FIGURE_DIR, exist_ok=True)

documents = []
debug_chunks = []

splitter = RecursiveCharacterTextSplitter(
    chunk_size=700,
    chunk_overlap=150,
    separators=["\n\n", "\n", ". ", " ", ""]
)

seen_figures = set()

print("[INFO] Chunk splitter initialized")


# ---------- PDF EXTRACTION ----------
print("\n[STEP] Extracting elements from PDF...\n")

elements = partition_pdf(
    filename="data/manual.pdf",
    strategy="hi_res",
    extract_images_in_pdf=True,
    infer_table_structure=True,
    languages=["eng"],
    hi_res_model_name="yolox"
)

print(f"[INFO] Total elements extracted: {len(elements)}")


# Debug: show all image paths detected
print("\n[DEBUG] Visual element paths detected:")
for el in elements:
    vis_path = getattr(el.metadata, "image_path", None)
    if vis_path:
        print(f"Page {el.metadata.page_number:3d} | {el.category:12} | {vis_path}")


page_text = {}
page_visuals = {}

print("\n[STEP] Organizing elements by page...\n")

for el in elements:

    page = el.metadata.page_number

    page_text.setdefault(page, "")
    page_visuals.setdefault(page, [])

    # ---------- TEXT ----------
    if hasattr(el, "text") and el.text and el.text.strip():
        page_text[page] += el.text + "\n"

    # ---------- VISUAL DETECTION ----------
    vis_path = getattr(el.metadata, "image_path", None)

    if vis_path and os.path.exists(vis_path):

        print(f"[INFO] Visual detected on page {page}: {vis_path}")

        try:
            with open(vis_path, "rb") as f:
                vis_bytes = f.read()
        except Exception as e:
            print(f"[ERROR] Cannot read {vis_path}: {e}")
            continue

        vis_hash = hashlib.md5(vis_bytes).hexdigest()

        if vis_hash in seen_figures:
            print("[INFO] Duplicate visual skipped")
            continue

        seen_figures.add(vis_hash)

        new_name = f"page-{page:03d}_{vis_hash[:12]}.png"
        new_path = os.path.join(EXTRACTED_FIGURE_DIR, new_name)

        try:
            shutil.copy2(vis_path, new_path)
            print(f"[INFO] Copied → {new_path}")
        except Exception as e:
            print(f"[ERROR] Copy failed {vis_path} → {new_path}: {e}")
            continue

        print("[INFO] Generating caption...")
        caption = generate_caption(new_path)

        if not caption or not caption.strip():
            print("[INFO] Caption empty → skipping")
            continue

        print(f"[INFO] Caption: {caption[:100]}")

        page_visuals[page].append({
            "path": new_path,
            "caption": caption,
            "original_path": vis_path,
            "hash": vis_hash,
            "page": page
        })


print("\n[STEP] Starting text chunking...\n")

for page_number in sorted(page_text.keys()):

    print(f"[INFO] Processing page {page_number}")

    text = page_text[page_number].strip()

    text = re.sub(r"[^A-Za-z0-9\s:/().,-]", " ", text)
    text = re.sub(r"\s+", " ", text)

    if not text.strip():
        print(f"[INFO] Page {page_number} has no usable text")
        continue

    chunks = splitter.split_text(text)

    print(f"[INFO] Page {page_number} → {len(chunks)} chunks")

    visuals = page_visuals.get(page_number, [])
    print(f"[INFO] Page {page_number} visuals: {len(visuals)}")

    for chunk_id, chunk in enumerate(chunks):

        chunk = chunk.strip()

        if len(chunk.split()) < 2:
            continue

        metadata = {
            "page": page_number,
            "chunk_id": chunk_id,
            "source": "manual.pdf",
            "visuals": visuals
        }

        documents.append(
            Document(
                page_content=chunk,
                metadata=metadata
            )
        )

        debug_chunks.append({
            "page": page_number,
            "chunk_id": chunk_id,
            "text_preview": chunk[:120] + "..." if len(chunk) > 120 else chunk,
            "visual_count": len(visuals),
            "visuals": [
                {
                    "path": v["path"],
                    "caption_preview": v["caption"][:60]
                }
                for v in visuals
            ]
        })


print("\n[STEP] Creating embeddings...\n")

embeddings = OpenAIEmbeddings()

print("[STEP] Creating FAISS vector store...")

if os.path.exists("vector_store"):
    shutil.rmtree("vector_store")

vectorstore = FAISS.from_documents(documents, embeddings)

vectorstore.save_local("vector_store")

print("[SUCCESS] Vector store saved")


print("\n[STEP] Saving debug chunk file...\n")

with open("chunks_debug.json", "w", encoding="utf-8") as f:
    json.dump(debug_chunks, f, indent=2, ensure_ascii=False)

print("[SUCCESS] Debug chunks saved")


print("\n========== INGESTION COMPLETE ==========\n")

print(f"[INFO] Total documents stored: {len(documents)}")
print(f"[INFO] Unique visuals processed: {len(seen_figures)}")
print(f"[INFO] Visuals saved in: {EXTRACTED_FIGURE_DIR}")
print(f"[INFO] Debug file: chunks_debug.json")