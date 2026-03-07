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



from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
import os
from config import OPENAI_API_KEY

embeddings = OpenAIEmbeddings()

vectorstore = FAISS.load_local(
    "vector_store",
    embeddings,
    allow_dangerous_deserialization=True
)

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


def ask_question(user_query):

    retriever = vectorstore.as_retriever(search_kwargs={"k": 8})

    docs = retriever.invoke(user_query)

    text_context = []
    images = []

    for doc in docs:

        if doc.metadata["type"] == "text":
            text_context.append(doc.page_content)

        if doc.metadata["type"] == "image":
            images.append(doc.metadata["image_path"])

    # remove duplicate images
    images = list(set(images))

    context = "\n".join(text_context)

    prompt = f"""
You are a car manual assistant.

Answer using only the context provided from the manual.
If the answer is not in the context, say you don't know.

Context:
{context}

Question:
{user_query}
"""

    response = llm.invoke(prompt)

    return {
        "text": response.content,
        "images": images
    }