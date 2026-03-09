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

from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from config import OPENAI_API_KEY


embeddings = OpenAIEmbeddings()

vectorstore = FAISS.load_local(
    "vector_store",
    embeddings,
    allow_dangerous_deserialization=True
)

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)


def ask_question(user_query):

    retriever = vectorstore.as_retriever(search_kwargs={"k": 10})

    docs = retriever.invoke(user_query)

    context_chunks = []
    images = []

    query_embedding = embeddings.embed_query(user_query)

    for doc in docs:

        context_chunks.append(doc.page_content)

        if "images" in doc.metadata:

            for img in doc.metadata["images"]:

                caption_embedding = embeddings.embed_query(img["caption"])

                similarity = sum(a*b for a, b in zip(query_embedding, caption_embedding))

                if similarity > 0.35:

                    images.append(img["path"])

    images = list(set(images))[:2]

    context = "\n\n".join(context_chunks)

    prompt = f"""
You are an assistant helping users understand a Honda car manual.

Use ONLY the context provided from the manual.

Context:
{context}

Question:
{user_query}

Answer clearly and concisely.
"""

    response = llm.invoke(prompt)

    return {
        "text": response.content,
        "images": images
    }