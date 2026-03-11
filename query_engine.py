# from langchain.vectorstores import FAISS
# from langchain_openai import OpenAIEmbeddings, ChatOpenAI

# embeddings = OpenAIEmbeddings()

# vectorstore = FAISS.load_local(
#     "vector_store",
#     embeddings,
#     allow_dangerous_deserialization=True
# )

# llm = ChatOpenAI(
#     model="gpt-4o-mini",
#     temperature=0
# )


# def ask_question(user_query):

#     retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

#     docs = retriever.get_relevant_documents(user_query)

#     context = "\n\n".join([doc.page_content for doc in docs])

#     prompt = f"""
# You are an assistant helping users understand a car manual.

# Use the provided context to answer clearly.

# Context:
# {context}

# Question:
# {user_query}
# """

#     response = llm.invoke(prompt)

#     image_path = None

#     keywords = ["show", "image", "diagram", "picture"]

#     if any(word in user_query.lower() for word in keywords):
#         image_path = docs[0].metadata.get("image_path")

#     return {
#         "text": response.content,
#         "image_path": image_path
#     }



# from langchain_community.vectorstores import FAISS
# from langchain_openai import OpenAIEmbeddings, ChatOpenAI
# import os
# from config import OPENAI_API_KEY

# embeddings = OpenAIEmbeddings()

# vectorstore = FAISS.load_local(
#     "vector_store",
#     embeddings,
#     allow_dangerous_deserialization=True
# )

# llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


# def ask_question(user_query):

#     retriever = vectorstore.as_retriever(search_kwargs={"k": 8})

#     docs = retriever.invoke(user_query)

#     text_context = []
#     images = []

#     for doc in docs:

#         if doc.metadata["type"] == "text":
#             text_context.append(doc.page_content)

#         if doc.metadata["type"] == "image":
#             images.append(doc.metadata["image_path"])

#     # remove duplicate images
#     images = list(set(images))

#     context = "\n".join(text_context)

#     prompt = f"""
# You are a car manual assistant.

# Answer using only the context provided from the manual.
# If the answer is not in the context, say you don't know.

# Context:
# {context}

# Question:
# {user_query}
# """

#     response = llm.invoke(prompt)

#     return {
#         "text": response.content,
#         "images": images
#     }

# from langchain_community.vectorstores import FAISS
# from langchain_openai import OpenAIEmbeddings, ChatOpenAI
# from config import OPENAI_API_KEY


# # ---------- LOAD VECTOR STORE ----------
# embeddings = OpenAIEmbeddings()

# vectorstore = FAISS.load_local(
#     "vector_store",
#     embeddings,
#     allow_dangerous_deserialization=True
# )


# # ---------- LLM ----------
# llm = ChatOpenAI(
#     model="gpt-4o-mini",
#     temperature=0
# )


# # ---------- MAIN QUERY FUNCTION ----------
# def ask_question(user_query):

#     # retrieve more docs for better recall
#     retriever = vectorstore.as_retriever(
#         search_kwargs={"k": 12}
#     )

#     docs = retriever.invoke(user_query)

#     text_context = []
#     images = []
#     relevant_pages = set()

#     # ---------- COLLECT TEXT ----------
#     for doc in docs:

#         if doc.metadata.get("type") == "text":

#             text_context.append(doc.page_content)

#             page = doc.metadata.get("page")

#             if page is not None:
#                 relevant_pages.add(page)

#     # ---------- COLLECT IMAGES FROM SAME PAGES ----------
#     for doc in docs:

#         if doc.metadata.get("type") == "image":

#             page = doc.metadata.get("page")

#             if page in relevant_pages:

#                 images.append(doc.metadata.get("image_path"))

#     # remove duplicates
#     images = list(set(images))

#     # limit number of images
#     images = images[:2]

#     context = "\n\n".join(text_context)

#     # ---------- PROMPT ----------
#     prompt = f"""
# You are an assistant helping users understand a Honda car manual.

# Use ONLY the provided context to answer the user's question.

# The context may come from:
# - diagram labels
# - manual text
# - control descriptions

# If the context includes diagram labels, explain where the component is located.

# If the answer cannot be found in the context, say:
# "I couldn't find that in the manual."

# Context:
# {context}

# Question:
# {user_query}

# Answer clearly and concisely.
# """

#     response = llm.invoke(prompt)

#     return {
#         "text": response.content,
#         "images": images
#     }

# from langchain_community.vectorstores import FAISS
# from langchain_openai import OpenAIEmbeddings, ChatOpenAI
# from config import OPENAI_API_KEY


# embeddings = OpenAIEmbeddings()

# vectorstore = FAISS.load_local(
#     "vector_store",
#     embeddings,
#     allow_dangerous_deserialization=True
# )

# llm = ChatOpenAI(
#     model="gpt-4o-mini",
#     temperature=0
# )


# def ask_question(user_query):

#     retriever = vectorstore.as_retriever(search_kwargs={"k": 10})

#     docs = retriever.invoke(user_query)

#     context_chunks = []
#     images = []

#     query_embedding = embeddings.embed_query(user_query)

#     for doc in docs:

#         context_chunks.append(doc.page_content)

#         if "images" in doc.metadata:

#             for img in doc.metadata["images"]:

#                 caption_embedding = embeddings.embed_query(img["caption"])

#                 similarity = sum(a*b for a, b in zip(query_embedding, caption_embedding))

#                 if similarity > 0.35:

#                     images.append(img["path"])

#     images = list(set(images))[:2]

#     context = "\n\n".join(context_chunks)

#     prompt = f"""
# You are an assistant helping users understand a Honda car manual.

# Use ONLY the context provided from the manual.

# Context:
# {context}

# Question:
# {user_query}

# Answer clearly and concisely.
# """

#     response = llm.invoke(prompt)

#     return {
#         "text": response.content,
#         "images": images
#     }


# from langchain_community.vectorstores import FAISS
# from langchain_openai import OpenAIEmbeddings, ChatOpenAI
# from langchain_core.documents import Document
# from config import OPENAI_API_KEY
# import math

# embeddings = OpenAIEmbeddings()

# vectorstore = FAISS.load_local(
#     "vector_store",
#     embeddings,
#     allow_dangerous_deserialization=True
# )

# llm = ChatOpenAI(
#     model="gpt-4o-mini",
#     temperature=0
# )


# def cosine_sim(v1, v2):
#     dot = sum(a * b for a, b in zip(v1, v2))
#     n1 = math.sqrt(sum(a * a for a in v1))
#     n2 = math.sqrt(sum(b * b for b in v2))
#     if n1 == 0 or n2 == 0:
#         return 0.0
#     return dot / (n1 * n2)


# def ask_question(user_query: str):
#     # 1. Use vectorstore similarity scores (fewer, better docs)
#     docs_and_scores = vectorstore.similarity_search_with_score(user_query, k=8)
#     # You can also drop very low‑score docs here if needed

#     context_chunks = []
#     candidate_images = []

#     # Precompute query embedding once
#     query_embedding = embeddings.embed_query(user_query)

#     for doc, _score in docs_and_scores:
#         context_chunks.append(doc.page_content)

#         # Your ingestion saved images under "images" key, not "visuals"
#         visuals = doc.metadata.get("images") or doc.metadata.get("visuals") or []

#         for vis in visuals:
#             caption = vis.get("caption", "")
#             if not caption:
#                 continue

#             caption_embedding = embeddings.embed_query(caption)
#             sim = cosine_sim(query_embedding, caption_embedding)

#             # Stricter threshold so we only keep *very* relevant images
#             if sim >= 0.75:
#                 candidate_images.append((sim, vis["path"]))

#     # Sort images by similarity and keep at most 1
#     candidate_images = sorted(candidate_images, key=lambda x: x[0], reverse=True)
#     selected_image_paths = [p for _, p in candidate_images[:1]]

#     context = "\n\n".join(context_chunks)

#     prompt = f"""
# You are an assistant helping users understand a Honda car manual.

# Use ONLY the context provided from the manual.
# Always answer in text form.
# If an image is provided separately by the tool, treat it only as an optional visual aid.
# Do NOT say things like "see the image below" unless you are certain the image is directly relevant.

# Context:
# {context}

# Question:
# {user_query}

# Answer clearly and concisely in text. If the context is not sufficient, say so explicitly.
# """

#     response = llm.invoke(prompt)

#     return {
#         "text": response.content,
#         "images": selected_image_paths  # may be [] or [one_path]
#     }


import math
from typing import Dict, Any, List, Tuple

from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.documents import Document
from config import OPENAI_API_KEY


# ====== Init ======
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.load_local("vector_store", embeddings, allow_dangerous_deserialization=True)
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


def cosine_sim(v1: List[float], v2: List[float]) -> float:
    dot = sum(a * b for a, b in zip(v1, v2))
    n1 = math.sqrt(sum(a * a for a in v1))
    n2 = math.sqrt(sum(b * b for b in v2))
    if n1 == 0 or n2 == 0:
        return 0.0
    return dot / (n1 * n2)


def ask_question(user_query: str) -> Dict[str, Any]:
    """
    1. Retrieve text chunks for the answer.
    2. Find candidate images via caption similarity.
    3. LLM generates text answer from chunks.
    4. LLM judges if candidate images are relevant to the answer.
    5. Return text + only truly relevant images.
    """

    # 1. Retrieve text context
    docs_and_scores = vectorstore.similarity_search_with_score(user_query, k=8)
    context_chunks = [doc.page_content for doc, _score in docs_and_scores]

    # 2. Find candidate images
    query_embedding = embeddings.embed_query(user_query)
    candidate_images = []

    for doc, _score in docs_and_scores:
        visuals = doc.metadata.get("images") or doc.metadata.get("visuals") or []
        for vis in visuals:
            caption = vis.get("caption", "")
            path = vis.get("path")
            if not caption or not path:
                continue

            caption_embedding = embeddings.embed_query(caption)
            sim = cosine_sim(query_embedding, caption_embedding)
            if sim >= 0.6:  # Reasonable relevance threshold
                candidate_images.append({"path": path, "caption": caption, "sim": sim})

    # 3. Generate text answer
    context = "\n\n".join(context_chunks)
    answer_prompt = f"""
Use ONLY the context provided from the Honda car manual.

Context:
{context}

Question:
{user_query}

Answer clearly and concisely in text.
"""
    answer_response = llm.invoke(answer_prompt)
    text_answer = answer_response.content

    # 4. Judge image relevance (only if we have candidates)
    final_images = []
    if candidate_images:
        # Sort by similarity
        candidate_images = sorted(candidate_images, key=lambda x: x["sim"], reverse=True)
        top_candidates = candidate_images[:3]  # Top 3 max

        # LLM judges: "Are these images relevant to my answer?"
        judge_prompt = f"""
You are judging image relevance for a Honda manual QA system.

Answer: {text_answer}
Question: {user_query}

Candidate images (captions):
{chr(10).join(f"• {img['caption']}" for img in top_candidates)}

For each image, respond with ONLY:
YES if this image is directly relevant to the answer above
NO if it is not needed or only vaguely related

Format exactly:
Image 1: YES/NO
Image 2: YES/NO  
Image 3: YES/NO

Be strict: only YES if the image clearly supports the specific answer.
"""
        judge_response = llm.invoke(judge_prompt)
        
        # Parse LLM judgment
        lines = judge_response.content.strip().split('\n')
        for i, line in enumerate(lines[:3]):
            if line.strip().startswith(f"Image {i+1}:"):
                if "YES" in line.upper():
                    final_images.append(top_candidates[i]["path"])

    return {
        "text": text_answer,
        "images": final_images  # 0–3 images, only LLM‑approved
    }
