from src.rag.rag_pipeline import ask

def chat(query):
    return ask(query)






# chat_service.py
#  │
#  ▼
# chat(query)
#  │
#  ▼
# ask(query)
#  │
#  ▼
# rag_pipeline.py