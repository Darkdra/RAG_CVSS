import os
import shutil

from langchain_community.document_loaders import DirectoryLoader
from langchain.schema import Document
from langchain_community.vectorstores import Chroma
from embeddings import CustomEmbeddings

CHROMA_PATH = "./chroma"
DATA_PATH = "./data/cves_text"


def main():
    documents = load_documents()
    save_to_chroma(documents)


def load_documents():
    print("Loading Directory", flush=True)
    loader = DirectoryLoader(DATA_PATH, glob="*.txt")
    documents = loader.load()
    print(len(documents))
    return documents


def save_to_chroma(documents: list[Document]):
    print("Saving to Chroma")
    # Clear out the database first.
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

    embedding_model = CustomEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L12-v2"
    )

    Chroma.from_documents(
        documents=documents, embedding=embedding_model, persist_directory=CHROMA_PATH
    )
    print(f"Saved {len(documents)} chunks to {CHROMA_PATH}.")


if __name__ == "__main__":
    main()
