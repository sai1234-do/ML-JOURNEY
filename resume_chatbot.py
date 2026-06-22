import streamlit as st
from docx import Document
from io import BytesIO
from sentence_transformers import SentenceTransformer
import chromadb
from transformers import pipeline

st.title("🤖 AI Resume Chatbot")

st.write("Upload your resume and ask questions.")

@st.cache_resource
def load_llm():

    return pipeline(
        "text2text-generation",
        model="google/flan-t5-base"
    )

llm = load_llm()

# Load embedding model once

@st.cache_resource
def load_model():
 return SentenceTransformer(
"sentence-transformers/all-MiniLM-L6-v2"
)

model = load_model()

uploaded_file = st.file_uploader(
"Upload Resume (.docx)",
type=["docx"]
)
if uploaded_file is None:

    st.info("Please upload a resume.")

    st.stop()

if uploaded_file is not None:


# Read Resume
  doc = Document(
    BytesIO(uploaded_file.getvalue())
)

# Create Chunks
full_text = ""

for para in doc.paragraphs:

    if para.text.strip():
        full_text += para.text.strip() + "\n"

words = full_text.split()

chunk_size = 100

chunks = []

for i in range(0, len(words), chunk_size):

    chunk = " ".join(
        words[i:i+chunk_size]
    )

    chunks.append(chunk)

st.success("Resume Loaded successfully✅")

# Create ChromaDB
client = chromadb.Client()

try:
    client.delete_collection( #delete if any previous data
        "resume_collection"
    )
except:
    pass

collection = client.create_collection(
    name="resume_collection"
)

# Store Chunks
for i, chunk in enumerate(chunks):

    embedding = model.encode(
        chunk
    ).tolist()

    collection.add(
        ids=[str(i)],
        embeddings=[embedding],
        documents=[chunk]
    )

st.success("Resume Indexed ✅")

# Ask Question
question = st.text_input(
    "Ask a question about the resume"
)

if st.button("Search"):

    query_embedding = model.encode(
        question
    ).tolist()

    results = collection.query(
        query_embeddings=[
            query_embedding
        ],
        n_results=1
    )

    st.subheader(
        "Answer"
    )

context = "\n".join(
    results["documents"][0]
)
prompt = f"""
You are a resume assistant.

Answer the question using the provided context.

Give a complete professional answer in 2-3 sentences.

Context:
{context}

Question:
{question}

Answer:
"""
response = llm(
    prompt,
    max_length=100
)

answer = response[0]["generated_text"]
st.subheader("🤖 Answer")

st.write(answer)

