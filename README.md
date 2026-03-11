# Multimodal RAG Chatbot for Car Manual

## Overview

This project builds a **Retrieval Augmented Generation (RAG) chatbot** that can answer questions from a car manual PDF.

Unlike a normal RAG system that only uses text, this project also retrieves **relevant images/diagrams from the manual** and shows them with the answer.

The system works in two main phases:

1. **Ingestion Pipeline** – prepares the PDF data for search
2. **Question Answering Pipeline** – answers user questions using the prepared data

---

# Project Architecture

PDF Manual
↓
Extract text + images
↓
Generate captions for images
↓
Split text into chunks
↓
Attach image metadata to chunks
↓
Create embeddings
↓
Store in FAISS vector database
↓
User asks question
↓
Retrieve relevant chunks
↓
Generate answer with LLM
↓
Filter relevant images
↓
Return answer + images

---

# Project Structure

```
XEBIA_RAG_CHATBOT
│
├── data/
│   └── manual.pdf                # Source car manual used for the chatbot
│
├── extracted_figures/            # Cleaned images copied from the PDF
├── extracted_images/             # Raw extracted visual elements
├── figures/                      # Temporary image storage during extraction
│
├── vector_store/                 # FAISS vector database (generated after ingestion)
│
├── venv/                         # Python virtual environment
│
├── .env                          # Environment variables (API keys)
├── .gitignore                    # Files ignored by Git
│
├── app.py                        # Entry point for running the chatbot application
├── caption_generation.py         # Generates captions for extracted images using a vision model
├── ingestion.py                  # Main ingestion pipeline that prepares the manual for RAG
├── query_engine.py               # Handles user questions and retrieves answers
│
├── chunks_debug.json             # Debug file showing text chunks and linked images
├── config.py                     # Stores configuration values such as API keys
├── requirements.txt              # Python dependencies for the project
├── test.py                       # Testing or experimentation file
```

---

# File Explanation

## ingestion_pipeline.py

This file prepares the PDF so it can be searched by the chatbot.

Main tasks:

1. Extract text, tables, and images from the PDF
2. Generate captions for each extracted image
3. Split text into smaller chunks
4. Attach images to the chunks of the same page
5. Convert chunks into embeddings
6. Store everything in a FAISS vector database

Output created:

* `vector_store/` → searchable vector database
* `extracted_figures/` → extracted images
* `chunks_debug.json` → debug file to inspect chunks

---

## caption_generation.py

This file generates **AI captions for images extracted from the manual**.

Example:

Image → Diagram of steering wheel buttons

Caption generated:

"Diagram showing steering wheel buttons for audio and cruise control"

These captions allow images to be searched using natural language.

---

## query_engine.py

This file answers user questions.

Steps performed:

1. Load FAISS vector database
2. Convert the user question into an embedding
3. Retrieve the most similar text chunks
4. Find candidate images using caption similarity
5. Generate an answer using the LLM
6. Ask the LLM to verify if the images are truly relevant
7. Return final text + relevant images

---

# How Image Retrieval Works

Each text chunk stores metadata like this:

```
{
  "page": 45,
  "chunk_id": 2,
  "visuals": [
    {
      "path": "extracted_figures/page-045_abc123.png",
      "caption": "Diagram showing fuse box location"
    }
  ]
}
```

When a question is asked:

1. The system compares the **question embedding** with the **caption embedding**.
2. If similarity is high, the image becomes a candidate.
3. The LLM then checks if the image actually helps answer the question.

Only relevant images are returned.

---

# Installation

## 1. Clone the repository

```
git clone <repo-url>
cd project
```

---

## 2. Create virtual environment

Windows

```
python -m venv venv
venv\\Scripts\\activate
```

Mac/Linux

```
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install dependencies

```
pip install -r requirements.txt
```

---

## 4. Add OpenAI API key

Create a file called `.env` or update `config.py`

Example:

```
OPENAI_API_KEY="your_api_key_here"
```

---

# Running the Project

## Step 1 – Run ingestion pipeline

This processes the manual and builds the vector database.

```
python ingestion_pipeline.py
```

This will:

* extract text
* extract images
* generate captions
* create vector embeddings
* store everything in FAISS

---

## Step 2 – Ask questions

Run the QA pipeline:

```
python query_engine.py
```

Example question:

```
How do I activate cruise control?
```

Output:

* Generated answer
* Relevant diagrams from the manual

---

# Important Concepts Used

## RAG (Retrieval Augmented Generation)

Instead of letting the LLM guess answers, the system first retrieves information from the manual and then generates an answer using that context.

---

## Embeddings

Embeddings convert text into vectors (lists of numbers).

This allows the system to compare similarity between:

* user questions
* manual text
* image captions

---

## Vector Database

FAISS stores embeddings and allows fast similarity search.

It helps find the most relevant chunks of the manual for a question.

---

## Multimodal Retrieval

The system retrieves:

* text
* diagrams

This makes answers more helpful for technical manuals.

---

# Debugging

You can inspect:

`chunks_debug.json`

This file shows:

* text chunks
* associated images
* page numbers

Useful for verifying ingestion.

---

# Example Output

Question:

"Where is the fuse box located?"

System response:

Text explanation + fuse box diagram.

---

# Future Improvements

Possible enhancements:

* Streamlit UI for chatbot
* Better image ranking
* Support for multiple manuals
* Hybrid search (keyword + embedding)

---

# Summary

This project builds a **multimodal RAG chatbot** that:

* reads a car manual
* understands diagrams
* retrieves relevant information
* generates accurate answers
* shows helpful images

It demonstrates how to combine:

* document processing
* vector search
* embeddings
* large language models

into a practical AI system.
