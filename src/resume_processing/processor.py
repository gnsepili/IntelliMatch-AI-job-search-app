"""Module for processing resumes."""

import logging
from typing import Dict, Any

import PyPDF2
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)

class ResumeProcessor:
    """Class to process resumes and generate embeddings."""

    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        """Initialize the ResumeProcessor with a specified model."""
        self.model = SentenceTransformer(model_name)

    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from a PDF file."""
        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = "".join(page.extract_text() for page in reader.pages)
            return text
        except Exception as e:
            logger.error(f"Error extracting text from PDF: {e}")
            raise

    def generate_embedding(self, text: str) -> Any:
        """Generate embedding from text."""
        try:
            return self.model.encode(text)
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            raise

    def process_resume(self, pdf_path: str) -> Dict[str, Any]:
        """Process resume and return text and embedding."""
        text = self.extract_text_from_pdf(pdf_path)
        embedding = self.generate_embedding(text)
        return {"text": text, "embedding": embedding}