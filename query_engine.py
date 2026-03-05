from langchain.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI

embeddings = OpenAIEmbeddings()
vectorstore = FAISS.load_local("vector_store", embeddings)

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def ask_question(user_query):
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
    docs = retriever.get_relevant_documents(user_query)

    context = "\n".join([doc.page_content for doc in docs])

    prompt = f"""
    Answer using context:

    {context}

    Question: {user_query}
    """

    response = llm.invoke(prompt)

    image_url = None
    keywords = ["show", "image", "diagram", "picture"]

    if any(word in user_query.lower() for word in keywords):
        image_url = docs[0].metadata.get("image_url")

    return {
        "text": response.content,
        "image_url": image_url
    }