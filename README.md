1. Project Title
# Departmental Store RAG Assistant



2. Project Description
An AI-powered departmental store assistant that helps users find product prices, stock availability, offers, and product locations using text and voice queries.



3. Features
- Product Search
- Price Check
- Stock Availability Check
- Product Location Finder
- Voice Chat Support
- Admin Dashboard
- CSV Data Upload
- RAG-based Product Retrieval



4. System Architecture
User
 ↓
Streamlit UI
 ↓
FastAPI
 ↓
Retriever
 ↓
ChromaDB
 ↓
LLM
 ↓
Response



5. Technology Stack
Frontend:
- Streamlit

Backend:
- FastAPI

Database:
- ChromaDB

Embeddings:
- BGE Embeddings

LLM:
- Mistral / Gemini / Groq

Voice:
- Whisper
- pyttsx3 or gTTS

Data Processing:
- Pandas
- OpenPyXL



6. Project Structure
project/
│
├── data/
├── logs/
├── src/
│   ├── api/
│   ├── services/
│   ├── rag/
│   ├── embeddings/
│   ├── utils/
│   └── core/
│
├── requirements.txt
├── main.py
└── README.md



7. Installation Steps
1. Clone the repository
2. Create virtual environment
3. Install requirements
4. Configure API keys
5. Run FastAPI
6. Run Streamlit



8. Usage Examples
User: How much banana?
Bot: Banana price is ₹45 per kg.

User: Where is banana?
Bot: Banana is available in Block A, Shelf 3.



9.RAG Architecture

**RAG Type:** Basic Vector RAG (Naive RAG)

**Data Source:** CSV Product Catalog

**Embedding Model:** BGE Embeddings

**Vector Database:** ChromaDB

**Retrieval Method:** Top-K Similarity Search

**LLM:** Mistral / Gemini / Groq (via LiteLLM)

### Flow

User Query → Query Embedding → ChromaDB Retrieval → Relevant Product Documents → Prompt Builder → LLM → Response





10. Voice Workflow
Voice Input
 ↓
Whisper (Speech-to-Text)
 ↓
RAG Pipeline
 ↓
LLM
 ↓
Text-to-Speech
 ↓
Voice Output




#####11. Future Enhancements
- User Login with OTP
- AI Voice Calling
- Automatic Order Placement
- Google Sheets Integration
- Multi-language Support
- Inventory Forecasting
- Automatic sms generate user and admin side


















