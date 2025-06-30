import pypdf
import docx2txt
import io
import os
import tempfile
import logging
from typing import Optional
from pathlib import Path


class DocumentParser:

    def __init__(self, logger: Optional[logging.Logger] = None):
        self.logger = logger or logging.getLogger(__name__)


    async def extract_text_from_file(self, file_content: bytes, filename: str) -> Optional[str]:

        self.logger.info(f"Extracting text from file {filename}")
        if not self._validate_inputs(file_content, filename):
            return None
        

        file_ext = Path(filename).suffix.lower().lstrip('.')

        extractors = {
            'pdf': self._extract_from_pdf,
            'docx': self._extract_from_docx,
            'doc': self._extract_from_docx
        }

        extractor = extractors.get(file_ext)

        if not extractor:
            self.logger.error(f"Format {file_ext} not supported")
            return None
        
        try:
            return extractor(file_content)
        except Exception as e:
            self.logger.error(f"Error extracting text from file {filename}: {str(e)}")
            return None
    
    def _validate_inputs(self, file_content: bytes, filename:str) -> bool:
        if not file_content:
            self.logger.error("File content is empty")
            return False
        
        if not filename or not Path(filename).suffix:
            self.logger.error(f"Filename {filename} is not valid")
            return False
        
        return True
    
    def _extract_from_pdf(self, file_content: bytes) -> Optional[str]:

        try:
            pdf_file = io.BytesIO(file_content)
            reader = pypdf.PdfReader(pdf_file)

            if len(reader.pages) == 0:
                self.logger.warning("PDF file is empty")
                return None
            
            extracted_text = []

            for page_num, page in enumerate(reader.pages):
                try:
                    page_text = page.extract_text()
                    if page_text and page_text.strip():
                        extracted_text.append(page_text.strip())
                except Exception as e:
                    self.logger.error(f"Error page {page_num}: {str(e)}")
            
            if not extracted_text:
                self.logger.warning("No text extracted from PDF")
                return None
            
            return "\n".join(extracted_text)
        
        except Exception as e:
            self.logger.error(f"Error extracting text from PDF: {str(e)}")
            return None
    
    def _extract_from_docx(self, file_content: bytes) -> Optional[str]:

        tmp_path = None
        try:
            with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as tmp_file:
                tmp_file.write(file_content)
                tmp_path = tmp_file.name

            text = docx2txt.process(tmp_path)

            if not text or not text.strip():
                self.logger.warning("No text extracted from DOCX")

            return text.strip() 
        
        except Exception as e:
            print(f"Error extracting text from DOCX: {str(e)}")
            return None
        
        finally:
            if tmp_path and os.path.exists(tmp_path):
                try:
                    os.unlink(tmp_path)
                except Exception as e:
                    self.logger.warning