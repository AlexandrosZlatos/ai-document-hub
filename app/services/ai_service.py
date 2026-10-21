import pdfplumber
import requests

def extract_text_from_pdf(file_path: str) -> str:
    text = ""
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
    except Exception as e:
        print(f"Error extracting text: {e}")
    return text

def generate_ai_summary(text: str) -> str:
    truncated_text = text[:4000] if len(text) > 4000 else text
    
    prompt = f"Please provide a concise and professional executive summary of the following document content in English:\n\n{truncated_text}"
    
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": prompt,
                "stream": False
            },
            timeout=60
        )
        if response.status_code == 200:
            return response.json().get("response", "No response generated.")
        else:
            return "Error communicating with local AI model."
    except Exception as e:
        return f"AI Service connection error: {str(e)}"