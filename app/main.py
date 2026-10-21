from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
import shutil
import os
from sqlalchemy.orm import Session

from app.database import engine, Base, get_db
from app.models import DocumentModel
from app.services.ai_service import extract_text_from_pdf, generate_ai_summary

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Document Processing & Workflow Hub",
    description="Backend API for automated document ingestion and AI analysis.",
    version="1.0.0"
)

UPLOAD_DIR = "uploaded_docs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Document Hub API! AI is ready."}

@app.post("/api/v1/documents/upload")
async def upload_document(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith((".pdf", ".txt", ".docx")):
        raise HTTPException(status_code=400, detail="Unsupported file format.")
    
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    extracted_text = ""
    if file.filename.endswith(".pdf"):
        extracted_text = extract_text_from_pdf(file_path)
    else:
        extracted_text = "Non-pdf text extraction pending..."

    ai_summary = "AI summary skipped (empty text)"
    if extracted_text and len(extracted_text.strip()) > 10:
        ai_summary = generate_ai_summary(extracted_text)

    db_document = DocumentModel(
        filename=file.filename,
        file_path=file_path,
        extracted_text=extracted_text,
        summary=ai_summary
    )
    
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    
    return {
        "id": db_document.id,
        "filename": db_document.filename,
        "summary": db_document.summary,
        "message": "File uploaded, processed by AI, and saved to PostgreSQL successfully!"
    }

@app.get("/api/v1/documents/")
def list_documents(db: Session = Depends(get_db)):
    documents = db.query(DocumentModel).all()
    return documents

@app.get("/api/v1/documents/{document_id}")
def get_document(document_id: int, db: Session = Depends(get_db)):
    document = db.query(DocumentModel).filter(DocumentModel.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found.")
    return document