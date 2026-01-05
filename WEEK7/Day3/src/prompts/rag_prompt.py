def get_rag_prompt(context, query):
    return f"""Context: {context}

Question: {query}

Answer based only on the context above:"""
