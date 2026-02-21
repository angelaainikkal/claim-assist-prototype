
# ClaimAssist (Prototype)

AI-powered insurance claim assistance system built using Streamlit and Gemini 1.5 Flash API.

## 📌 Problem Statement
Automate and simplify medical insurance claim submission while generating structured, regulator-ready summaries using AI.

## 🚀 Features (Prototype)
- Upload medical documents (PDF/Image)
- OCR-based text extraction
- AI-powered claim summarization using Gemini 1.5 Flash
- Preliminary fraud/risk flagging
- Interactive Streamlit dashboard

## 🛠 Tech Stack

### Application Layer
- Python
- Streamlit

### AI Layer
- Gemini 1.5 Flash API (LLM-based summarization & reasoning)
- Prompt-engineered structured outputs

### Data Processing
- Pandas
- OCR (pytesseract)

## 🔗 Gemini Integration Logic
1. Extracted document text is cleaned and structured.
2. Prompt template is dynamically generated.
3. Text is sent to Gemini 1.5 Flash API.
4. Response is parsed into:
   - Claim summary
   - Risk indicators
   - Missing document flags

## ⚙️ How to Run

1. Clone the repository
2. Add your Gemini API key in `.env`
3. Install dependencies:
   pip install -r requirements.txt
   
   pip install streamlit
5. Run:
   .\venv\Scripts\activate
   streamlit run app.py

## 🔐 Environment Variable
Create a `.env` file:

GEMINI_API_KEY=your_api_key_here

## 👩‍💻 Team

ParallelX

