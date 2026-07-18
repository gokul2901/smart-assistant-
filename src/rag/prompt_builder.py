def build_prompt(query, context):

    return f"""
    Context:
    {context}

    User Question:
    {query}

    Answer using only context.
    """