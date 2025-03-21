import streamlit as st
from qdrant_client import QdrantClient, models
from fastembed.embedding import TextEmbedding,DefaultEmbedding
from transformers import T5ForConditionalGeneration, T5Tokenizer
from qdrant_client.models import VectorParams, Distance, PointStruct
import os


client = QdrantClient(":memory:")
embedding_model = DefaultEmbedding()
st.title("QDrant test")


# Read document
with open("data.txt", "r") as f:
    docs = f.read().split("\n")  # Split into lines

#print(f"Documents List: {docs}")

embeddings = list(embedding_model.embed(docs))

# Embedding size
embedding_size = len(embeddings[0]) 

if not client.collection_exists(collection_name="admissions"):
    client.create_collection(
    collection_name="admissions",
    vectors_config=VectorParams(size=len(embeddings[0]), distance=Distance.COSINE),
)

points = [
    PointStruct(
        id=i,
        vector=embedding.tolist(),
        payload={"text": doc}
    )
    for i, (embedding,doc) in enumerate(zip(embeddings,docs))
]


client.upsert(
    collection_name="admissions",
    points=points
)

model = T5ForConditionalGeneration.from_pretrained('t5-base')
tokenizer = T5Tokenizer.from_pretrained('t5-base')


# Define function to generate prompt
def generate_prompt(query, retrieved_docs):
    return f"Use the following information to answer the question: {retrieved_docs}\n\nQuestion: {query}"


def generate_answer(query_text):
    query_embedding = list(embedding_model.embed([query_text]))[0]
    
    search_results = client.search(
    collection_name="admissions",
    query_vector=query_embedding,
    limit=5
    )
    
    retrieved_docs = "\n".join([doc.payload["text"] for doc in search_results])

    prompt = generate_prompt(query_text, retrieved_docs)

    inputs = tokenizer(prompt,return_tensors = "pt")
    output = model.generate(**inputs)
    
    return tokenizer.decode(output[0], skip_special_tokens=True)

st.subheader("Ask a question about the admissions process")
query_text = st.text_input("Enter your question here:")

st.subheader("Answer:")
answer = generate_answer(query_text)
st.write(answer)