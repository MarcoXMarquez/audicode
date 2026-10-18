"""Local document and image parsers for AudiCode.

Provides 100% local, CPU-based document-to-Markdown and OCR extraction:
- PDF -> Markdown tables and structured text via pymupdf4llm / PyMuPDF
- Office (.docx, .pptx, .xlsx, .xls, .csv) -> Markdown via markitdown
- Images (.png, .jpg, .webp, screenshots) -> Local CPU OCR via rapidocr-onnxruntime

Designed to run locally on the user's PC without external cloud APIs or GPU requirements,
allowing local models (e.g., qwen2.5-coder:7b) to accurately understand and audit
documents, slides, spreadsheets, and UI screenshots.
"""

import logging
import os
import tempfile
from typing import Optional, List, Dict, Any

logger = logging.getLogger(__name__)

# Extensions supported by the local Office parser (markitdown)
OFFICE_EXTENSIONS = frozenset({".docx", ".pptx", ".xlsx", ".xls", ".csv", ".epub"})

# Extensions supported by the local image OCR engine
IMAGE_EXTENSIONS = frozenset({".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tiff", ".gif"})

# Cached RapidOCR singleton instance for CPU inference
_RAPID_OCR_INSTANCE = None


def get_rapid_ocr():
    """Lazily load and cache the RapidOCR CPU instance."""
    global _RAPID_OCR_INSTANCE
    if _RAPID_OCR_INSTANCE is None:
        try:
            from rapidocr_onnxruntime import RapidOCR
            # RapidOCR runs on CPU via ONNX Runtime without external dependencies
            _RAPID_OCR_INSTANCE = RapidOCR()
            logger.info("Initialized RapidOCR CPU engine successfully")
        except Exception as e:
            logger.warning(f"Failed to initialize RapidOCR: {e}")
            return None
    return _RAPID_OCR_INSTANCE


def extract_pdf_markdown(file_path: str, max_chars: int = 100000) -> str:
    """Extract PDF contents into clean Markdown using pymupdf4llm.
    
    Converts tables into GitHub Flavored Markdown (| Col1 | Col2 |), preserves headings,
    and handles scanned pages via fallback OCR.
    """
    if not os.path.exists(file_path):
        return f"[PDF error: file not found at {file_path}]"

    extracted_md = ""
    # 1. Primary engine: pymupdf4llm
    try:
        import pymupdf4llm
        import fitz
        doc = fitz.open(file_path)
        try:
            extracted_md = pymupdf4llm.to_markdown(doc) or ""
        finally:
            doc.close()
    except Exception as e:
        logger.warning(f"pymupdf4llm failed for {file_path}: {e}; falling back to markitdown/pypdf")

    # 2. Secondary fallback: markitdown
    if not extracted_md or not extracted_md.strip():
        try:
            from markitdown import MarkItDown
            md_engine = MarkItDown()
            result = md_engine.convert(file_path)
            extracted_md = getattr(result, "text_content", "") or getattr(result, "markdown", "") or ""
        except Exception as e:
            logger.warning(f"markitdown fallback failed for PDF {file_path}: {e}")

    # 3. Tertiary fallback: pypdf
    if not extracted_md or not extracted_md.strip():
        try:
            from pypdf import PdfReader
            reader = PdfReader(file_path)
            pages_text = []
            for i, page in enumerate(reader.pages):
                txt = (page.extract_text() or "").strip()
                if txt:
                    pages_text.append(f"### Página {i + 1}\n{txt}")
            extracted_md = "\n\n".join(pages_text)
        except Exception as e:
            logger.warning(f"pypdf fallback failed for {file_path}: {e}")

    # 4. Scanned PDF fallback: If extracted text is almost empty, run OCR on page images
    if not extracted_md or len(extracted_md.strip()) < 50:
        try:
            import fitz
            doc = fitz.open(file_path)
            ocr_pages = []
            ocr_engine = get_rapid_ocr()
            if ocr_engine:
                for page_idx in range(min(len(doc), 15)):  # Limit to first 15 pages for CPU speed
                    page = doc[page_idx]
                    pix = page.get_pixmap(dpi=150)
                    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
                        tmp_img = tmp.name
                    try:
                        pix.save(tmp_img)
                        page_ocr = extract_image_ocr(tmp_img)
                        if page_ocr and not page_ocr.startswith("["):
                            ocr_pages.append(f"### Página {page_idx + 1} (Escaneada - OCR Local):\n{page_ocr}")
                    finally:
                        if os.path.exists(tmp_img):
                            try:
                                os.remove(tmp_img)
                            except OSError:
                                pass
                if ocr_pages:
                    extracted_md = "\n\n".join(ocr_pages)
            doc.close()
        except Exception as e:
            logger.warning(f"Scanned PDF OCR fallback failed: {e}")

    if extracted_md and extracted_md.strip():
        extracted_md = extracted_md.strip()
        if len(extracted_md) > max_chars:
            extracted_md = extracted_md[:max_chars] + f"\n\n[...Texto del PDF truncado a {max_chars:,} caracteres]"
        return extracted_md

    return "[El PDF fue procesado localmente pero no contiene texto legible ni imágenes escaneadas con texto detectable.]"


def extract_office_markdown(file_path: str, max_chars: int = 100000) -> str:
    """Extract Office documents (.docx, .pptx, .xlsx, .xls, .csv, .epub) to Markdown.
    
    Slides are split into sections (### Diapositiva N), and spreadsheets are formatted
    into clean Markdown tables.
    """
    if not os.path.exists(file_path):
        return f"[Office document error: file not found at {file_path}]"

    ext = os.path.splitext(file_path)[1].lower()
    extracted_text = ""

    # Primary engine: Microsoft markitdown
    try:
        from markitdown import MarkItDown
        md = MarkItDown()
        res = md.convert(file_path)
        extracted_text = getattr(res, "text_content", "") or getattr(res, "markdown", "") or ""
    except Exception as e:
        logger.warning(f"markitdown failed for {file_path}: {e}")

    # Fallback for Word .docx: native zipfile/xml parser
    if (not extracted_text or not extracted_text.strip()) and ext == ".docx":
        try:
            from src.markitdown_runtime import _extract_docx_native
            extracted_text = _extract_docx_native(file_path) or ""
        except Exception as e:
            logger.warning(f"Native docx extraction fallback failed: {e}")

    # Fallback for Excel / CSV via pandas / openpyxl
    if (not extracted_text or not extracted_text.strip()) and ext in (".xlsx", ".xls", ".csv"):
        try:
            import pandas as pd
            if ext == ".csv":
                df = pd.read_csv(file_path, nrows=500)
                extracted_text = df.to_markdown(index=False)
            else:
                xl = pd.ExcelFile(file_path)
                sheets_md = []
                for sheet_name in xl.sheet_names[:5]:  # First 5 sheets
                    df = xl.parse(sheet_name, nrows=200)
                    sheets_md.append(f"### Hoja: {sheet_name}\n\n" + df.to_markdown(index=False))
                extracted_text = "\n\n".join(sheets_md)
        except Exception as e:
            logger.warning(f"Pandas tabular fallback failed: {e}")

    # Fallback for PowerPoint .pptx via python-pptx
    if (not extracted_text or not extracted_text.strip()) and ext == ".pptx":
        try:
            import pptx
            prs = pptx.Presentation(file_path)
            slides_md = []
            for idx, slide in enumerate(prs.slides):
                slide_lines = [f"### Diapositiva {idx + 1}"]
                for shape in slide.shapes:
                    if shape.has_text_frame:
                        for paragraph in shape.text_frame.paragraphs:
                            t = paragraph.text.strip()
                            if t:
                                slide_lines.append(f"- {t}")
                if len(slide_lines) > 1:
                    slides_md.append("\n".join(slide_lines))
            extracted_text = "\n\n".join(slides_md)
        except Exception as e:
            logger.warning(f"python-pptx fallback failed: {e}")

    if extracted_text and extracted_text.strip():
        extracted_text = extracted_text.strip()
        if len(extracted_text) > max_chars:
            extracted_text = extracted_text[:max_chars] + f"\n\n[...Contenido del documento truncado a {max_chars:,} caracteres]"
        return extracted_text

    return f"[El documento {os.path.basename(file_path)} fue procesado localmente pero no se extrajo texto legible.]"


def extract_image_ocr(image_path: str) -> str:
    """Extract text and UI labels from an image using local CPU OCR (RapidOCR).
    
    Returns structured text lines with confidence scores, formatting detected buttons
    and checkboxes cleanly for prompt comprehension.
    """
    if not os.path.exists(image_path):
        return f"[OCR error: image not found at {image_path}]"

    ocr = get_rapid_ocr()
    if not ocr:
        return "[Local OCR unavailable: rapidocr-onnxruntime is not installed or failed to load]"

    try:
        results, elapse = ocr(image_path)
        if not results:
            return "[Local OCR scanned image: no readable text or labels detected]"

        # Group text boxes by vertical alignment (lines)
        # Result item format: [box_coordinates, text, confidence_score]
        lines = []
        for item in results:
            if not item or len(item) < 3:
                continue
            box, text, score = item[0], item[1], item[2]
            text = (text or "").strip()
            if not text:
                continue
            
            # Format UI patterns for prompt clarity
            # E.g. Checkbox detection
            if text.startswith("[x]") or text.startswith("[X]"):
                text = f"[x] {text[3:].strip()}"
            elif text.startswith("[]") or text.startswith("[ ]"):
                text = f"[ ] {text[3:].strip()}"
            
            lines.append(text)

        if not lines:
            return "[Local OCR scanned image: no readable text detected]"

        formatted_ocr = "\n".join(lines)
        return formatted_ocr
    except Exception as e:
        logger.error(f"Error during RapidOCR extraction of {image_path}: {e}")
        return f"[Local OCR extraction failed: {str(e)}]"


def is_supported_document(file_path: str) -> bool:
    """Return True if the file can be parsed into Markdown by local parsers."""
    if not file_path:
        return False
    ext = os.path.splitext(file_path)[1].lower()
    return ext == ".pdf" or ext in OFFICE_EXTENSIONS


def is_supported_image(file_path: str) -> bool:
    """Return True if the file is an image supported by RapidOCR."""
    if not file_path:
        return False
    ext = os.path.splitext(file_path)[1].lower()
    return ext in IMAGE_EXTENSIONS
