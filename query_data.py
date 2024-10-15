from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
from langchain_chroma import Chroma
from embeddings import CustomEmbeddings

CHROMA_PATH = "./chroma"

PROMPT_TEMPLATE = """
Given the following example vulnerabilities:

{examples}

---

Explain a possible Confidentiality, Integrity and Availability impact of this vulnerability: {question}
"""


def main():
    query_text = input("Vulnerability To Triage:")

    # Prepare the DB.
    embedding_model = CustomEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L12-v2"
    )
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_model)

    # Search the DB.
    results = db.similarity_search_with_relevance_scores(query_text)
    if len(results) == 0:
        print(f"Unable to find matching results.")
        return

    example_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)

    model = OllamaLLM(model="llama3.2")
    chain = prompt | model
    response_text = chain.invoke({"examples": example_text, "question": query_text})

    sources = [doc.metadata.get("source", None) for doc, _score in results]
    formatted_response = f"Response: {response_text}\n\nSources: {sources}"
    print(formatted_response)


if __name__ == "__main__":
    main()
