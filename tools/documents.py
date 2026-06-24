@tool
def query_documents(query: str) -> str:
    """Use this to query documents and return text with source filenames."""
    results = vectorstore.similarity_search_with_score(query, k=2)
    
    responses = []
    for doc, score in results:
        # Assuming metadata contains the filename
        source = doc.metadata.get("source", "Unknown Source")
        responses.append(f"Content: {doc.page_content} (Source: {source})")
        
    return "\n".join(responses)